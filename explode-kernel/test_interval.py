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
numba.extending.make_attribute_wrapper(IntervalType, "hi", "hi")

@numba.extending.overload_attribute(IntervalType, "width")
def get_width(interval):
    def getter(interval):
        return interval.hi - interval.lo
    return getter

@numba.extending.lower_builtin(Interval, numba.types.Float, numba.types.Float)
def impl_interval(context, builder, sig, args):
    typ = sig.return_type
    lo, hi = args
    interval = numba.cgutils.create_struct_proxy(typ)(context, builder)
    interval.lo = lo
    interval.hi = hi
    return interval._getvalue()

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
