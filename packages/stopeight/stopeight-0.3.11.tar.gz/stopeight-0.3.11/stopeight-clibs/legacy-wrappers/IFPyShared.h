#undef NDEBUG
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

#include "turnanalyzer.h"
#include <stopeight-clibs/shared_types.h>
#include <stopeight-clibs/Matrix.h>

class QListWrapper : public ListSwitchable<dpoint>
{
  public:
    QListWrapper(py::array_t<sp::timecode<double>, py::array::c_style> other);
    template<class inType> QListWrapper(inType& other);
    using ListSwitchable<dpoint>::ListSwitchable;

    py::array_t<sp::timecode<double>, py::array::c_style> toPyArray();
};

//template TurnAnalyzer<dpoint>::TurnAnalyzer(QListWrapper& list);
class TurnAnalyzerWrapper : public TurnAnalyzer<dpoint>
{
  public:
    template<class inType> TurnAnalyzerWrapper(inType &other);
};