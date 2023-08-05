// Copyright (C) 2019 Fassio Blatter
// GNU Lesser General Public License, version 2.1
#include "stopeight-clibs/shared_types.h"

namespace analyzer {

template <typename T, size_t Size = 2,
          typename = typename std::enable_if_t<std::is_pod<sp::timecode<T, Size>>::value>>
class result : public std::vector<sp::timecode<T, Size>>
{ //is not gonna be a numpy_dtype -> no pod needed
public:
    result() : std::vector<sp::timecode<T, Size>>(){}; //todo: delete -> proper allocation
    result(size_t n) : std::vector<sp::timecode<T, Size>>(n)
    {
        auto tc = sp::timecode<T, Size>{};
        tc.__init({0, 0});
        std::fill(std::begin(*this), std::end(*this), tc);
    };
    result(std::initializer_list<T>) = delete;

    //only for numpy test at the moment
    bool invalid = false;
    int cycle_count = 0;
    //next*
};

template<typename T> using it_pair = std::pair< typename result<T>::iterator, typename result<T>::iterator >;

}
