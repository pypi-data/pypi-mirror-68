from typing import List, Dict, Union

from cpython.mem cimport PyMem_Malloc, PyMem_Free
import numpy as np
from . cimport c_tpu


cdef class TPUPlaceholder:
    cdef const c_tpu.TPUIONode *_ptr


cpdef parse_placeholder_description(placeholder: TPUPlaceholder):
    """Parses metadata description to Python dictionary"""
    cdef const c_tpu.TPUIONode *desc = placeholder._ptr
    result = dict()
    result['address'] = desc.address
    result['scale'] = [scale for scale in desc.scale[:desc.scale_len]]
    result['user_shape'] = [axis for axis in desc.user_shape[:desc.user_shape_len]]
    result['user_shape_len'] = desc.user_shape_len
    result['user_order'] = desc.user_order

    padding_intermediate = <list>desc.padding
    result['padding'] = [tuple(dic.values()) for dic in padding_intermediate[:desc.user_shape_len]]
    tpu_shape_intermediate = <list>desc.tpu_shape
    result['tpu_shape'] = tpu_shape_intermediate[:desc.user_shape_len]
    result['tpu_order'] = desc.tpu_order
    result['tpu_shape_len'] = desc.tpu_shape_len
    result['dtype'] = desc.dtype
    result['layer_name'] = desc.anchor.decode('utf-8') if desc.anchor else desc.layer_name.decode('utf-8')
    result['size'] = desc.size
    return result


class TPUProgramException(Exception):
    pass


class TPUDeviceException(Exception):
    pass


class NOTPUDeviceException(TPUDeviceException):
    pass


cdef class TPUProgram:
    cdef c_tpu.TPUProgram* c_tpu_program
    cdef c_tpu.TPUProgramZipLoader *c_loader

    def __cinit__(self, path: str):
        cdef b_path = path.encode("utf-8")
        cdef char *c_path = b_path
        self.c_loader = c_tpu.tpu_program_zip_loader_open(c_path)

        if not self.c_loader:
            raise TPUProgramException("Failed to open program file %s" % path)

        self.c_tpu_program = c_tpu.tpu_program_open(self.c_loader)
        if not self.c_tpu_program:
            raise TPUProgramException("Failed to open TPU program")

    def __dealloc__(self):
        if self.c_loader:
            c_tpu.tpu_program_zip_loader_close(self.c_loader)

        if self.c_tpu_program:
            c_tpu.tpu_program_close(self.c_tpu_program)

    @property
    def inputs_count(self):
        return <int>c_tpu.tpu_program_get_inputs_count(self.c_tpu_program)

    @property
    def outputs_count(self):
        return <int>c_tpu.tpu_program_get_outputs_count(self.c_tpu_program)

    @property
    def inputs(self):
        """Returns verbose description of input parameters"""
        return [self.get_input_description(i) for i in range(self.inputs_count)]

    @property
    def outputs(self):
        """Returns verbose description of output parameters"""
        return [self.get_output_description(i) for i in range(self.outputs_count)]

    def get_input_name(self, index):
        py_byte_str = c_tpu.tpu_program_get_input_name_by_index(self.c_tpu_program, index)
        return py_byte_str.decode('utf-8')

    def get_input_size(self, index):
        return <int>c_tpu.tpu_program_get_input_buffer_size(self.c_tpu_program, index)

    def get_output_name(self, index):
        py_byte_str =  c_tpu.tpu_program_get_output_name_by_index(self.c_tpu_program, index)
        return py_byte_str.decode('utf-8')

    def get_output_size(self, index):
        return <int>c_tpu.tpu_program_get_output_buffer_size(self.c_tpu_program, index)

    def get_input_description(self, index):
        """Returns verbose description of network input"""
        cdef TPUPlaceholder wrapper = TPUPlaceholder.__new__(TPUPlaceholder)
        wrapper._ptr = c_tpu.tpu_program_get_input_node(self.c_tpu_program, index)
        return parse_placeholder_description(wrapper)

    def get_output_description(self, index):
        """Returns verbose description of network output"""
        cdef TPUPlaceholder wrapper = TPUPlaceholder.__new__(TPUPlaceholder)
        wrapper._ptr = c_tpu.tpu_program_get_output_node(self.c_tpu_program, index)
        return parse_placeholder_description(wrapper)

    @property
    def driver_version(self):
        py_byte_str =  c_tpu.tpu_program_get_driver_version(self.c_tpu_program)
        if py_byte_str:
            return py_byte_str.decode('utf-8')

    @property
    def ip_version(self):
        py_byte_str =  c_tpu.tpu_program_get_ip_version(self.c_tpu_program)
        if py_byte_str:
            return py_byte_str.decode('utf-8')


np_to_tpu_type = {np.dtype('int8'): 0,
                  np.dtype('float32'): 1,
                  np.dtype('float16'): 2,
                  np.dtype('float64'): 3}

MAX_TENSORS = 32


cdef class TPUDevice:
    cdef c_tpu.TPUDevice* c_tpu_device
    cdef c_tpu.TPUProgram* c_tpu_program

    cdef c_tpu.tpu_io_descriptor* io_descriptor

    def __cinit__(self):
        self.c_tpu_device = c_tpu.tpu_device_build()
        if not self.c_tpu_device:
            raise NOTPUDeviceException()
        self.program = None
        self.io_descriptor = NULL

    def __init__(self):
        self.program = None
        self.io_dict_mode = 0

    def __dealloc__(self):
        if self.c_tpu_device:
            c_tpu.tpu_device_close(self.c_tpu_device)

        if self.io_descriptor:
            c_tpu.tpu_io_descriptor_free(self.io_descriptor)

    def load(self, program: TPUProgram):
        if c_tpu.tpu_program_check_hardware_parameters(self.c_tpu_device, program.c_tpu_program) != 0:
            raise TPUProgramException("Program compiled for different device")

        rc = c_tpu.tpu_program_load(self.c_tpu_device, program.c_tpu_program)

        if rc != 0:
            raise TPUProgramException("Failed to load program")

        self.program = program
        self.c_tpu_program = program.c_tpu_program
        self.io_descriptor = c_tpu.tpu_io_descriptor_create(self.c_tpu_program)

    def get_input_tensor_dict(self, features: Dict[str, np.ndarray]):
        for name, tensor in features.items():
            py_bytes = name.encode('utf-8')
            index = c_tpu.tpu_program_get_input_index_by_name(self.c_tpu_program, <char *>py_bytes)
            if index < 0:
                    raise TPUProgramException(f"input layer name {name} not found")
            yield index, tensor

    def get_input_tensor_list(self, features: List[np.ndarray]):
        for index, tensor in enumerate(features):
            yield index, tensor

    def get_features_iterator(self, features):
        getter = None
        if type(features) == dict:
            self.io_dict_mode = 1
            getter = self.get_input_tensor_dict(features)
        elif type(features) == list:
            self.io_dict_mode = 0
            getter = self.get_input_tensor_list(features)
        if getter is None:
            raise TPUProgramException("Expected dict or list as features")
        return getter

    def set_features(self, features: List[np.ndarray] or Dict[str, np.ndarray]):
        features_count = len(features)
        assert features_count == <int>c_tpu.tpu_program_get_inputs_count(self.c_tpu_program)

        feature_getter = self.get_features_iterator(features)

        allowed_types = (np.int8, np.float32, np.float64)
        cdef c_tpu.TPUTensor feature_tensors[32]

        for index, tensor in feature_getter:
            if tensor.dtype not in allowed_types:
                raise TPUProgramException("unexpected tensor type %s. Expected %s" % (tensor.dtype, allowed_types))

            input_bytes = tensor.tobytes()
            feature_tensors[index] = c_tpu.tpu_program_make_input_user_tensor(self.c_tpu_program, index)
            feature_tensors[index].data = <char *>input_bytes
            feature_tensors[index].size = len(input_bytes)
            feature_tensors[index].dtype = np_to_tpu_type[tensor.dtype]
                
        with nogil:
            for i in range(features_count):
                rc = c_tpu.tpu_program_set_input_tensor(self.c_tpu_program, self.io_descriptor, &feature_tensors[i], i)
                if rc != 0:
                    raise TPUProgramException(f"can't set input tensor {i}")

    def get_results(self, dtype = np.int8) -> List[np.ndarray]:
        cdef c_tpu.TPUTensor result_tensors[32]
        output_count = c_tpu.tpu_program_get_outputs_count(self.c_tpu_program)
        for i in range(output_count):
            result_tensors[i] = c_tpu.tpu_program_make_output_user_tensor(self.c_tpu_program, i)
            result_tensors[i].dtype = np_to_tpu_type[np.dtype(dtype)]
            result_tensors[i].size = c_tpu.tpu_tensor_get_size(&result_tensors[i])
            result_tensors[i].data = <char *>PyMem_Malloc(result_tensors[i].size)
            if not result_tensors[i].data:
                raise MemoryError

        with nogil:
            for i in range(output_count):
                c_tpu.tpu_program_get_output_tensor(self.c_tpu_program, self.io_descriptor, &result_tensors[i], i)

        cdef char* c_buffer
        try:
            if self.io_dict_mode == 1:
                result = dict()
            else:
                result = []

            for i in range(output_count):
                shape = []
                for j in range(result_tensors[i].shape_len):
                    shape.append(result_tensors[i].shape[j])
                c_buffer = <char *>result_tensors[i].data
                buffer = c_buffer[:result_tensors[i].size]
                arr = np.frombuffer(buffer, dtype=np.dtype(dtype)).reshape(shape)
                if self.io_dict_mode == 1:
                    result_name = c_tpu.tpu_program_get_output_name_by_index(self.c_tpu_program, i)
                    result[result_name.decode('utf-8')] = arr
                else:
                    result.append(arr)
            return result
        finally:
            for i in range(output_count):
                PyMem_Free(result_tensors[i].data)

    def set_input_buffer(self, buffer: bytes, index: int) -> None:
        """
        Set input buffer by index
        """
        cdef char* c_buffer = <char *>buffer
        c_tpu.tpu_program_set_input_buffer(self.io_descriptor, index, c_buffer, len(buffer))

    def get_output_buffer(self, index: int) -> bytes:
        """
        Get output buffer by index
        """
        cdef char *output = <char *>c_tpu.tpu_program_get_output_buffer(self.io_descriptor, index)
        cdef bytes b = output[:c_tpu.tpu_program_get_output_buffer_size(self.c_tpu_program, index)]
        return b

    def run_inference(self):
        with nogil:
            inference_entry = c_tpu.tpu_inference_submit(self.c_tpu_device, self.io_descriptor)
            rc = c_tpu.tpu_inference_wait(self.c_tpu_device)
        return rc

    def run(self, features: List[np.ndarray] or Dict[str, np.ndarray],
            dtype = np.int8) -> List[np.ndarray] or Dict[str, np.ndarray]:
        assert self.program is not None
        self.set_features(features)
        rc = self.run_inference()
        if rc != 0:
            raise TPUProgramException("TPU {} Program execution failed".format(self.program))
        return self.get_results(dtype=dtype)

    def _run_raw_list(self, inputs: List[bytes]) -> List[bytes]:
        for i, buffer in enumerate(inputs):
            self.set_input_buffer(buffer, i)
        rc = self.run_inference()
        if rc != 0:
            raise TPUProgramException("TPU {} Program execution failed".format(self.program))

        result = list()
        for i in range(c_tpu.tpu_program_get_outputs_count(self.c_tpu_program)):
            buffer = self.get_output_buffer(i)
            result.append(buffer)
        return result

    def _set_buffer_by_name(self, name, buf):
        py_bytes = name.encode('utf-8')
        cdef const char *c_name = <const char *>py_bytes
        i = c_tpu.tpu_program_get_input_index_by_name(self.c_tpu_program, c_name)
        self.set_input_buffer(buf, i)

    def _run_raw_dict(self, inputs: Dict[str, bytes]) -> Dict[str, bytes]:
        for name, buf in inputs.items():
            self._set_buffer_by_name(name, buf)

        rc = self.run_inference()
        if rc != 0:
            raise TPUProgramException("TPU {} Program execution failed".format(self.program))
        result = dict()
        for i in range(c_tpu.tpu_program_get_outputs_count(self.c_tpu_program)):
            buffer = self.get_output_buffer(i)
            name = c_tpu.tpu_program_get_output_name_by_index(self.c_tpu_program, i)
            result[name.decode('utf-8')] = buffer
        return result

    def run_raw(self, inputs: Dict[str, bytes] or List[bytes]):
        input_count = c_tpu.tpu_program_get_inputs_count(self.c_tpu_program)
        assert len(inputs) == input_count, f"Expected {input_count} inputs, got {len(inputs)}"

        if type(inputs) == list:
            return self._run_raw_list(inputs)
        elif type(inputs) == dict:
            return self._run_raw_dict(inputs)

        raise TPUProgramException("Expected list or dict of inputs")

    @property
    def hardware_id(self):
        return <int>c_tpu.tpu_get_hardware_id(self.c_tpu_device)

    @property
    def control_unit_version(self):
        return <int>c_tpu.tpu_get_control_unit_version(self.c_tpu_device)

    @property
    def ewp_banks_count(self):
        return <int>c_tpu.tpu_get_ewp_banks_count(self.c_tpu_device)

    @property
    def ewp_bank_size(self):
        return <int>c_tpu.tpu_get_ewp_bank_size(self.c_tpu_device)

    @property
    def psp_buffer_size(self):
        return <int>c_tpu.tpu_get_psp_buffer_size(self.c_tpu_device)

    @property
    def ddr_banks_count(self):
        return <int>c_tpu.tpu_get_ddr_banks_count(self.c_tpu_device)

    @property
    def ddr_bank_size(self):
        return <int>c_tpu.tpu_get_ddr_bank_size(self.c_tpu_device)

    @property
    def axi_word_length(self):
        return <int>c_tpu.tpu_get_axi_word_length(self.c_tpu_device)

    @property
    def cache_word_length(self):
        return <int>c_tpu.tpu_get_cache_word_length(self.c_tpu_device)

    @property
    def cache_bank_size(self):
        return <int>c_tpu.tpu_get_cache_bank_size(self.c_tpu_device)

    @property
    def cache_banks_count(self):
        return <int>c_tpu.tpu_get_cache_banks_count(self.c_tpu_device)

    @property
    def systolic_array_size(self):
        cdef c_tpu.int_pair p = c_tpu.tpu_get_systolic_array_size(self.c_tpu_device)
        return <int>p.first, <int>p.second

    @property
    def driver_version(self):
        py_byte_str =  c_tpu.tpu_get_driver_version(self.c_tpu_device)
        if py_byte_str:
            return py_byte_str.decode('utf-8')

    @property
    def ip_version(self):
        py_byte_str =  c_tpu.tpu_get_ip_version(self.c_tpu_device)
        if py_byte_str:
            return py_byte_str.decode('utf-8')
