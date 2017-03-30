import pickle

import numpy
a = numpy.array(range(10), dtype=numpy.double)
b = numpy.ones(10, dtype=numpy.double)

import numba
import numba.npyufunc.dufunc
import numba.compiler
import numba.dispatcher

def something(x):
    return x*x

vec = numba.npyufunc.dufunc.DUFunc(something, targetoptions={"nopython": True})
cres = vec.add("f8(f8)")
# something_fast = vec.build_ufunc()
print(vec(a))

print(cres.library._compiled_object)

def other(x):
    return x**3

vec2 = numba.npyufunc.dufunc.DUFunc(other, targetoptions={"nopython": True})
cres2 = vec2.add("f8(f8)")
# other_fast = vec2.build_ufunc()
print(vec2(a))



serialized = cres._reduce()
pickle.dump(serialized, open("serialized.pkl", "wb"))

#####################################

import pickle
import time

import numba
import numba.npyufunc.dufunc.DUFunc
import numba.compiler
import numba.dispatcher

import whatever

def regular_compilation():
    startTime = time.time()
    vec = numba.npyufunc.dufunc.DUFunc(whatever.whatever, targetoptions={"nopython": True})
    cres = vec.add("f8(f8)")
    print(time.time() - startTime)

regular_compilation()

serialized = pickle.load(open("serialized.pkl", "rb"))

class FromSerialized(numba.dispatcher.NullCache):
    def __init__(self, serialized):
        self.serialized = serialized
    def load_overload(self, sig, target_context):
        return numba.compiler.CompileResult._rebuild(target_context, *self.serialized)

def reconstitution():
    startTime = time.time()
    new_vec = numba.npyufunc.dufunc.DUFunc(whatever.whatever)
    ONE = time.time()
    new_vec._dispatcher.cache = FromSerialized(serialized)
    TWO = time.time()
    cres2 = new_vec.add("f8(f8)")
    THREE = time.time()
    new_vec.disable_compile()
    FOUR = time.time()
    something_fast = new_vec.build_ufunc()
    FIVE = time.time()
    print(ONE - startTime)
    print(TWO - startTime)
    print(THREE - startTime)
    print(FOUR - startTime)
    print(FIVE - startTime)

reconstitution()

# import numpy
# a = numpy.array(range(10), dtype=numpy.double)
# something_fast(a)




################################################

import ctypes
lib = ctypes.cdll.LoadLibrary("femtocode/fromroot/_fastreader.so")


import numpy
a = numpy.array(range(10), dtype=numpy.float64) 

from femtocode.fromroot._fastreader import make_ufunc

ptr = ctypes.addressof(ctypes.cast(lib.exported, ctypes.POINTER(ctypes.c_char)).contents)

f = make_ufunc(ptr)

f(a)






import ctypes
import numba

@numba.jit("f8(f8)", nopython=True)
def example(x):
  return x + 1.1

cres = example.overloads.values()[0]

numba.targets.codegen.CodeLibrary._dump_elf(cres.library._compiled_object)
# __main__.example$1.float64
# cpython.__main__.example$1.float64

cres.library._compiled_object

ptr = cres.library._codegen._engine.get_function_address("cpython.__main__.example$1.float64")

# cfunc = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(ptr)

class PyTypeObject(ctypes.Structure):
    _fields_ = ("ob_refcnt", ctypes.c_int), ("ob_type", ctypes.c_void_p), ("ob_size", ctypes.c_int), ("tp_name", ctypes.c_char_p)
 
class PyObject(ctypes.Structure):
    _fields_ = ("ob_refcnt", ctypes.c_int), ("ob_type", ctypes.POINTER(PyTypeObject))
 
PyObjectPtr = ctypes.POINTER(PyObject)

a = 3.14

cfunc = ctypes.CFUNCTYPE(PyObjectPtr, PyObjectPtr)(ptr)
cfunc(ctypes.cast(id(a), PyObjectPtr))







import ctypes


ctypes.cast(lib.exported, ctypes.POINTER(ctypes.c_char))[0:10]


ptr2 = cres.library._codegen._engine.get_function_address("__main__.something$1.float64")


ff = _dynfunc.make_function(__import__("__main__"), "something", "doc", ptr2, cres.environment, (cres.library,))

ff(a, b)  # nope: SystemError: error return without exception set


cfunc = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(ptr2)


class PyTypeObject(ctypes.Structure):
    _fields_ = ("ob_refcnt", ctypes.c_int), ("ob_type", ctypes.c_void_p), ("ob_size", ctypes.c_int), ("tp_name", ctypes.c_char_p)
 
class PyObject(ctypes.Structure):
    _fields_ = ("ob_refcnt", ctypes.c_int), ("ob_type", ctypes.POINTER(PyTypeObject))
 
PyObjectPtr = ctypes.POINTER(PyObject)


# cfunc = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(ptr2)

cfunc = ctypes.CFUNCTYPE(PyObjectPtr, PyObjectPtr, PyObjectPtr)(ptr2)
cfunc(ctypes.cast(id(a), PyObjectPtr), ctypes.cast(id(b), PyObjectPtr))



################################################

#include <stdio.h>
#include <numpy/ufuncobject.h>
#include <numpy/npy_3kcompat.h>

static void testy(char** args, npy_intp* dimensions, npy_intp* steps, void* data) {
  npy_intp i = 0;
  npy_intp n = dimensions[0];

  char* in = args[0];
  char* out = args[1];

  npy_intp in_step = steps[0];
  npy_intp out_step = steps[1];

  for (;  i < n;  i++) {
    *((double*)out) = *(double*)in * *(double*)in;
    in += in_step;
    out += out_step;
  }
}

extern "C" {
  void exported(char** args, npy_intp* dimensions, npy_intp* steps, void* data) {
    npy_intp i = 0;
    npy_intp n = dimensions[0];

    char* in = args[0];
    char* out = args[1];

    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];

    for (;  i < n;  i++) {
      *((double*)out) = *(double*)in * *(double*)in;
      in += in_step;
      out += out_step;
    }
  }
}


PyUFuncGenericFunction npytest[1] = {&testy};
static char types[2] = {NPY_DOUBLE, NPY_DOUBLE};
static void* data[1] = {NULL};

size_t pointer;

static PyObject* make_ufunc(PyObject* self, PyObject* args) {
  if (!PyArg_ParseTuple(args, "l", &pointer))
    return NULL;

  printf("pointer %ld\n", pointer);

  return PyUFunc_FromFuncAndData((PyUFuncGenericFunction*)(&pointer), data, types, 1, 1, 1, PyUFunc_None, "generated", "generated docstring", 0);
}

    // testy testy testy testy testy testy testy testy
    import_umath();
    PyObject* pytesty = PyUFunc_FromFuncAndData(npytest, data, types, 1, 1, 1, PyUFunc_None, "testy", "testy_docstring", 0);
    PyObject* d = PyModule_GetDict(module);
    PyDict_SetItemString(d, "testy", pytesty);
    Py_DECREF(pytesty);
    // testy testy testy testy testy testy testy testy





################################################


from __future__ import print_function

import time

from ctypes import CFUNCTYPE, c_double

import llvmlite.binding as llvm


# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one

llvm_ir = """
   ; ModuleID = "examples/ir_fpadd.py"
   target triple = "unknown-unknown-unknown"
   target datalayout = ""

   define double @"fpadd"(double %".1", double %".2")
   {
   entry:
     %"res" = fadd double %".1", %".2"
     ret double %"res"
   }
   """

def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    mpm = llvm.PassManagerBuilder()
    mpm.opt_level = 3L
    pm = llvm.ModulePassManager()
    mpm.populate(pm)
    pm.run(mod)
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    return mod

# elfstring = None

# def _object_compiled_hook(ll_module, buf):
#     global elfstring
#     print("_object_compiled_hook")
#     print(ll_module)
#     elfstring = buf

# def _object_getbuffer_hook(ll_module):
#     print("_object_getbuffer_hook")
#     print(ll_module)

# elfstring = open("/tmp/downloads/fpadd2.elf", "rb").read()
elfstring = open("/tmp/downloads/example.elf", "rb").read()

def _object_compiled_hook(ll_module, buf):
    global elfstring
    print("_object_compiled_hook")
    print(ll_module)
    # elfstring = buf

def _object_getbuffer_hook(ll_module):
    global elfstring
    print("_object_getbuffer_hook")
    print(ll_module)
    return elfstring

ZERO = time.time()
engine = create_execution_engine()

ONE = time.time()

engine.set_object_cache(_object_compiled_hook, _object_getbuffer_hook)

TWO = time.time()

# mod = compile_ir(engine, llvm_ir)
engine.finalize_object()

THREE = time.time()


func_ptr = engine.get_function_address("__main__.example$1.float64")

import ctypes
pdouble = ctypes.c_double * 1
out = pdouble()

pointerType = ctypes.POINTER(None)
dummy1 = pointerType()
dummy2 = pointerType()

cfunc = ctypes.CFUNCTYPE(ctypes.c_int32, pdouble, pointerType, pointerType, ctypes.c_double)(func_ptr)
cfunc(out, dummy1, dummy2, ctypes.c_double(3.14))

print(out[0])



# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("fpadd")

FOUR = time.time()

# Run the function via ctypes
cfunc = CFUNCTYPE(c_double, c_double, c_double)(func_ptr)
cfunc(1.0, 3.5)

FIVE = time.time()

print("ONE - ZERO {}".format(ONE - ZERO))
print("TWO - ONE {}".format(TWO - ONE))
print("THREE - TWO {}".format(THREE - TWO))
print("FOUR - THREE {}".format(FOUR - THREE))
print("FIVE - FOUR {}".format(FIVE - FOUR))





NO OPTIMIZATION PASS    OPTIMIZATION LEVEL 3    DIRECTLY FROM CACHE
=====================================================================
>>> ONE - ZERO          >>> ONE - ZERO          >>> ONE - ZERO       
0.003571033477783203    0.0035619735717773438   0.0035669803619384766
>>> TWO - ONE           >>> TWO - ONE           >>> TWO - ONE        
0.0025320053100585938   0.002613067626953125    0.0026290416717529297
>>> THREE - TWO         >>> THREE - TWO         >>> THREE - TWO      
0.008620977401733398    0.012457847595214844    0.0027849674224853516
>>> FOUR - THREE        >>> FOUR - THREE        >>> FOUR - THREE     
0.0034170150756835938   0.003377199172973633    0.0033860206604003906
>>> FIVE - FOUR         >>> FIVE - FOUR         >>> FIVE - FOUR      
0.0036160945892333984   0.003715991973876953    0.0037789344787597656





NO OPTIMIZATION PASS
=================================
ONE - ZERO 0.00167298316956
TWO - ONE 4.10079956055e-05
THREE - TWO 0.0071861743927
FOUR - THREE 0.00019097328186
FIVE - FOUR 0.000128984451294

ONE - ZERO 0.00171089172363
TWO - ONE 4.19616699219e-05
THREE - TWO 0.00722408294678
FOUR - THREE 0.000166893005371
FIVE - FOUR 0.000153064727783

OPTIMIZATION LEVEL 3
=================================
ONE - ZERO 0.00170397758484
TWO - ONE 4.31537628174e-05
THREE - TWO 0.010370016098
FOUR - THREE 0.000197887420654
FIVE - FOUR 0.000116109848022

ONE - ZERO 0.0016770362854
TWO - ONE 3.91006469727e-05
THREE - TWO 0.010321855545
FOUR - THREE 0.000177145004272
FIVE - FOUR 0.0001540184021

DIRECTLY FROM CACHE
=================================
ONE - ZERO 0.00168704986572
TWO - ONE 4.10079956055e-05
THREE - TWO 0.000380992889404
FOUR - THREE 0.000136137008667
FIVE - FOUR 0.000109910964966

ONE - ZERO 0.00163888931274
TWO - ONE 4.10079956055e-05
THREE - TWO 0.000429153442383
FOUR - THREE 0.000136852264404
FIVE - FOUR 0.000111103057861
