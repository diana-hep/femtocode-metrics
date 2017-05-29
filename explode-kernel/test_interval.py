import numba

class Interval(object):
    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi

    def __repr__(self):
        return "Interval({}, {})".format(self.lo, self.hi)

    @property
    def width(self):
        return self.hi - self.lo

class IntervalType(numba.types.Type):
    def __init__(self):
        super(IntervalType, self).__init__(name="Interval")

intervaltype = IntervalType()

@numba.extending.typeof_impl.register(Interval)
def typeof_index(val, c):
    return intervaltype

@numba.extending.type_callable(Interval)
def type_interval(context):
    def typer(lo, hi):
        if isinstance(lo, numba.types.Float) and isinstance(hi, numba.types.Float):
            return intervaltype
    return typer

@numba.extending.register_model(IntervalType)
class IntervalModel(numba.extending.models.StructModel):
    def __init__(self, dmm, fe_type):
        members = [("lo", numba.types.float64), ("hi", numba.types.float64)]
        super(IntervalModel, self).__init__(dmm, fe_type, members)

numba.extending.make_attribute_wrapper(IntervalType, "lo", "lo")
# numba.extending.make_attribute_wrapper(IntervalType, "hi", "hi")

@numba.extending.infer_getattr
class StructAttribute(numba.typing.templates.AttributeTemplate):
    key = IntervalType
    def generic_resolve(self, typ, attr):
        if attr == "hi":
            return numba.types.float64

@numba.extending.lower_getattr(IntervalType, "hi")
def struct_getattr_impl(context, builder, typ, val):
    val = numba.cgutils.create_struct_proxy(typ)(context, builder, value=val)
    return numba.targets.imputils.impl_ret_borrowed(context, builder, numba.types.float64, val.hi)

@numba.extending.lower_setattr(IntervalType, "hi")
def struct_setattr_impl(context, builder, sig, args):
    assert isinstance(sig.args[0], IntervalType)
    assert isinstance(sig.args[1], numba.types.Float)
    interval, newvalue = args
    val = numba.cgutils.create_struct_proxy(sig.args[0])(context, builder, value=interval)
    ptr = val._get_ptr_by_name("hi")
    return builder.store(newvalue, ptr)




@numba.extending.overload_attribute(IntervalType, "width")
def get_width(interval):
    def getter(interval):
        return interval.hi - interval.lo
    return getter

@numba.extending.overload_method(IntervalType, "wonky")
def interval_wonky(interval, arg):
    if isinstance(arg, numba.types.Float):
        def wonky_impl(interval, arg):
            return Interval(interval.lo - arg, interval.hi)
        return wonky_impl

@numba.extending.overload_method(IntervalType, "wonky2")
def interval_wonky2(interval, arg):
    if isinstance(arg, numba.types.Float):
        def wonky2_impl(interval, arg):
            interval.lo -= arg
            return interval
        return wonky2_impl

@numba.extending.overload_method(IntervalType, "getiter")
def interval_iter(interval):
    def iter_impl(interval):
        return [1, 2, 3]
    return iter_impl

@numba.extending.lower_builtin(Interval, numba.types.Float, numba.types.Float)
def impl_interval(context, builder, sig, args):
    typ = sig.return_type
    lo, hi = args
    interval = numba.cgutils.create_struct_proxy(typ)(context, builder)
    interval.lo = lo
    interval.hi = hi
    return interval._getvalue()

def changelo(interval):
    interval.lo = interval.lo - 10

@numba.extending.lower_builtin(changelo, Interval)
def impl_changelo(context, builder, sig, args):
    interval, = args
    interval.lo = interval.lo - 10

@numba.extending.unbox(IntervalType)
def unbox_interval(typ, obj, c):
    lo_obj = c.pyapi.object_getattr_string(obj, "lo")
    hi_obj = c.pyapi.object_getattr_string(obj, "hi")
    interval = numba.cgutils.create_struct_proxy(typ)(c.context, c.builder)
    interval.lo = c.pyapi.float_as_double(lo_obj)
    interval.hi = c.pyapi.float_as_double(hi_obj)
    c.pyapi.decref(lo_obj)
    c.pyapi.decref(hi_obj)
    is_error = numba.cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return numba.extending.NativeValue(interval._getvalue(), is_error=is_error)

@numba.extending.box(IntervalType)
def box_interval(typ, val, c):
    interval = numba.cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val)
    lo_obj = c.pyapi.float_from_double(interval.lo)
    hi_obj = c.pyapi.float_from_double(interval.hi)
    class_obj = c.pyapi.unserialize(c.pyapi.serialize_object(Interval))
    res = c.pyapi.call_function_objargs(class_obj, (lo_obj, hi_obj))
    c.pyapi.decref(lo_obj)
    c.pyapi.decref(hi_obj)
    c.pyapi.decref(class_obj)
    return res

@numba.njit
def doit1():
    i = Interval(4.4, 6.4)
    return i.width
print doit1()

@numba.njit
def doit2():
    i = Interval(4.4, 6.4)
    return i.lo + i.hi
print doit2()

@numba.njit
def doit3(i):
    return i.width
print doit3(Interval(4.4, 6.4))

@numba.njit
def doit4():
    return Interval(4.4, 6.4)
print doit4()

@numba.njit
def doit5(i):
    return i
print doit5(Interval(4.4, 6.4))

@numba.njit
def doit6(i):
    i.hi = 99.999
    return i.width
print doit6(Interval(4.4, 6.4))

@numba.njit
def doit7(i):
    return i.wonky(10.0)
print doit7(Interval(4.4, 6.4))

# @numba.njit
# def doit8(i):
#     return i.wonky2(10.0)
# print doit8(Interval(4.4, 6.4))

# @numba.njit
# def doit8(interval):
#     out = 0
#     for j in interval:
#         out += j
#     return out
# print doit8(Interval(4.4, 16.4))

# print "HERE"
# @numba.njit
# def doit9(i):
#     changelo(i)
#     return i
# print doit9(Interval(4.4, 6.4))

print
print "DOIT10"

@numba.njit
def doit10():
    interval = Interval(4.4, 6.4)
    interval.hi = 99.999
    return interval.width
print doit10()

# cres = doit10.overloads.values()[0]
# print cres.library.get_llvm_str()




# define i32 @"__main__.doit10$10."(double* noalias nocapture %retptr, { i8*, i32 }** noalias nocapture %excinfo, i8* noalias nocapture readnone %env) {
# entry:
#   %.51 = alloca double, align 8
#   %excinfo.1 = alloca { i8*, i32 }*, align 8
#   store double 0.000000e+00, double* %.51, align 8
#   %.53 = call i32 @"__main__.getter$2.Interval"(double* nonnull %.51, { i8*, i32 }** nonnull %excinfo.1, i8* null, double 4.400000e+00, double 6.400000e+00)
#   switch i32 %.53, label %B0.if [
#     i32 -2, label %B0.endif
#     i32 0, label %B0.endif
#   ] 

# B0.if:                                            ; preds = %entry
#   %0 = bitcast { i8*, i32 }** %excinfo.1 to i64*
#   %.541 = load i64, i64* %0, align 8
#   %1 = bitcast { i8*, i32 }** %excinfo to i64*
#   store i64 %.541, i64* %1, align 8
#   ret i32 %.53

# B0.endif:                                         ; preds = %entry, %entry
#   %2 = bitcast double* %.51 to i64*
#   %.632 = load i64, i64* %2, align 8
#   %3 = bitcast double* %retptr to i64*
#   store i64 %.632, i64* %3, align 8
#   ret i32 0
# } 
