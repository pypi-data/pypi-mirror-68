#include "git.h"
#include <IFPyShared.h>
#undef NDEBUG
#include <pybind11/stl.h>
//cant remove opaque; no custom caster vector -> array?
PYBIND11_MAKE_OPAQUE(std::vector<sp::timecode<double>>);

#include "turns.h"
#include "spirals.h"
#include "cliffs.h"

std::vector<size_t> transform_indices(QList<dpoint> result_qt){
    auto result = std::vector<size_t>();
    //gcc: auto or  windows: decltype
    std::transform(std::begin(result_qt),std::end(result_qt),std::back_inserter(result),[](dpoint& it_in){
        return size_t(it_in.position);
    });
    return result;
}

PYBIND11_MODULE(finders, f){
	if(GitMetadata::Populated()) {
		object sha;
	        if(GitMetadata::AnyUncommittedChanges()) {
			sha = cast(GitMetadata::CommitSHA1()+"+dirty");
	        } else {
			sha = cast(GitMetadata::CommitSHA1());
		}
		f.attr("version") = sha;
	}
        //static QList<dpoint> findTurns(ListCopyable<dpoint> toBeProcessed);
        f.def("Turns",[](QList<dpoint>& in)->std::vector<size_t>{
            return transform_indices(Turns<dpoint>::findTurns(in));
        });
        f.def("Spirals",[](QList<dpoint>& in)->std::vector<size_t>{
            return transform_indices(Spirals<dpoint>::findSpiralCliffs(in));
        });
        f.def("Cliffs",[](QList<dpoint>& in)->std::vector<size_t>{
            return transform_indices(Cliffs<dpoint>::findCliffs(in));
        });
}
