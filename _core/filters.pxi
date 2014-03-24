

cdef extern from "Filters.h" namespace "lime":
    cdef cppclass Filter:
        Filter()

    cdef cppclass BlurFilter(Filter):
        BlurFilter()
        BlurFilter(int quality, int blur_x, int blur_y)

    cdef cppclass ColorMatrixFilter(Filter):
        ColorMatrixFilter(QuickVec[float] matrix)

    cdef cppclass DropShadowFilter(BlurFilter):
        DropShadowFilter(int quality, int blur_x, int blur_y,
                            double theta, double distance, int color, 
                                double strength, double alpha, bool hide, 
                                    bool knockout, bool inner)

cdef _to_native_filter_list(py_filter_list):
    cdef Filter *ret
    cdef QuickVec[float] matrix

    for py_filter in py_filter_list:
        cname = py_filter.__class__.__name__
        if cname == 'BlurFilter':
            ret = new BlurFilter(py_filter.quality, py_filter.blurX, 
                                                        py_filter.blurY)
        elif cname == 'ColorMatrixFilter':
            for val in py_filter.matrix:
                matrix.push_back(val)
            ret = new ColorMatrixFilter(matrix)

        elif cname == 'DropShadowFilter':
            ret = new DropShadowFilter(
                    py_filter.quality, py_filter.blurX, py_filter.blurY,
                        py_filter.angle, py_filter.distance, py_filter.color, 
                            py_filter.strength, py_filter.alpha, 
                                py_filter.hideObject, py_filter.knockout, 
                                    py_filter.inner)