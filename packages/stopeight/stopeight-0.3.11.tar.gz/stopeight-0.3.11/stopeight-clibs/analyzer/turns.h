// Copyright (C) 2019 Fassio Blatter
// GNU Lesser General Public License, version 2.1
#include "stopeight-clibs/analyzer.h"
#include "stopeight-clibs/shared_types.h"

#include <thread>
#include <list>

namespace analyzer {
    //    predicate contains hardcoded type
    //    returns a bool
    /*template<typename Coords_T> class predicate : std::function<bool(result<Coords_T>&)>{
    public:
        predicate()=delete;
        virtual const sp::tctype type()=0;
        virtual bool operator()(result<Coords_T>& segment)=0;
    };
    template<typename Coords_T> class legal_segment : predicate<Coords_T>{
    public:
        sp::tctype type(){return sp::tctype::LEGALSEGMENT;}
        bool operator()(result<Coords_T>& segment){
            if (segment.size()>2){
                //do nothing -> notFoundOne
                //throw std::logic_error("Minimum common size for all predicates is ?");
            }
            return false;
        }
    };
    template<typename Coords_T> const predicate<Coords_T> predicate_sequence_1[1] = {&legal_segment<Coords_T>{}};

    // predicate will return true on n+1
    template<class Iterator
    //,typename = typename std::enable_if_t<std::is_base_of<std::contiguous_iterator_tag, typename std::iterator_traits<Iterator>::iterator_category>::value>
    > void predicate_exec(Iterator start,Iterator growingEnd,Iterator partition_end,bool& foundOne,bool& absolute_index,predicate<typename std::iterator_traits<Iterator>::value_type>& predicate){//return by reference not tie
        auto result = std::find_if(start,growingEnd,&predicate);//capture incremental->transform2?
        ////HEAD AND TAIL NEED TO BE IN PREDICATE?
        //if (result!=partition_end){
        //    foundOne = true;
        //    absolute_index = std::distance(start,end-head);
        //    type = predicate::tctype
        //    //break: avoid continuing predicate sequence because of possible exceptions?
        //}
    }*/

    
    /*

    template<typename T> using partition_bounds = typename std::array<std::random_access_iterator<result<T>>,2>;

    //    copies data to thread and handles indexes
    template<class T> class ThreadedFunctor : public sp::readonly_functor<void(void)>,
                                                public std::vector<T>{//takes two iterators, returns one (head and tail corrected); needs templated? TYPE
        public:
        ThreadedFunctor(size_t head=1, size_t tail=0) : std::vector<T>(),head(head),tail(tail),foundOne(false),cancel(false),reachedEnd(false),terminated(false){
        }
//        returnvalue should be absoluteindex, but thread ignores returnvalue
        void operator()(){
            //kernel starts here: allocate clean copy and rotation temporary
            foundOne = false;
            cancel = false;
            auto const start = std::begin(*this);
            auto end = start+1;
            while(!cancel && !foundOne && end++ != std::end(*this)){
                //for predicate in predicate_sequence
                    predicate_exec(start,growingEnd,std::end(*this))
                    //refresh rotation temporary
            }
            //kernel ends here
            if (!foundOne && !cancel)
                reachedEnd = true;//equals notFoundOne -> deplete
            terminated = true;
        }
        bool cancel;
        bool foundOne:
        bool reachedEnd;
        bool terminated;
        size_t absolute_index;
        enum type;
        private:

        size_t head,tail;
    };

    // prototyping:
    //    input function which returns index, analyzer::result
    //    output analyzer::result with annotated timecodes
    // aim when fully working:
    //    input function cycle style sequence
    //    output analyzer::result with final type annotation after completed cycle

    // sets hardcoded type from predicate
    template<class T> class ThreadPool {
	    public:
        ThreadPool(unsigned int n = std::thread::hardware_concurrency()) : numThreads(n), threads(std::list<std::thread>()){
        }
        ~ThreadPool(){
            running=false;
        };
        result<T> operator()(result<T> input, predicate_sequence& predicate) {
            auto const partition_size = input.size();
            for (int i=0;i<numThreads;i++){
                auto partition_start = std::begin(input)+i*partition_size;
                auto partition_end = std::end(input)+(i+1)*partition_size;
                if (i!=0)
                    partition_start--;
                if (i==numThreads-1)
                    partition_end = std::end(input);
                auto functor = ThreadedFunctor<decltype(T::coords)>(1,0,predicate_sequence);
                std::copy(partition_start,partition_end,std::begin(functor));//todo implicit convert timecode -> coords: no POD
                threads.append(functor,std::thread(functor));//pass by value, preinitialize or pass by reference?
            }
//            while (threadsleft){
//                mark threadsleft false
//                for thread in threads
//                    if thread finished and foundone
//                        if coincides with end or previously marked type
//                            wash out: refill previous
//                        else
//                            complexity: refill
//                                get tail
//                                get next threads spresult
//                                stop next thread
//                                two new threads with halfnhalf
//                                mark in input (TYPE!!)
//                                mark threadsleft
//                                break
//                    if thread finished and not foundone
//                        deplete
//                    if thread not finished
//                        mark threadsleft
//            }

        }
        private:
        std::list<std::pair<ThreadedFunctor<decltype(T::coords)>,std::thread>> threads;
        unsigned int numThreads;
        bool running = false;
    };*/
}
