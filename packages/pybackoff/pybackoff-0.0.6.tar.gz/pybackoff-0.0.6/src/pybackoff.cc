#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>
#include <map>
#include <tuple>
#include <vector>
#include <string>
#include <utility> 
#include <iostream>
#include <fstream>
#include <functional> 
#include <iomanip>
#include <cmath>
#include <ctime>
#include <algorithm> 


typedef std::tuple<std::string, std::string, std::string> Trigram;
typedef std::vector<float> Sequence;

const uint64_t FNV_PRIME = 0x100000001b3;
const uint64_t FNV_OFFSET_BASIS = 0xcbf29ce484222325;

namespace py = pybind11;

class Logger {
public:
    static void log(const std::string& msg);
};

void Logger::log(const std::string& msg) {
    std::time_t now = std::time(0);
    char* dt = std::ctime(&now);
    std::cout << "\r" << dt << "] " << msg;
}

class Ngrams {

private:
    std::map<uint64_t, float> counts;
    size_t size = 0;

    template<typename... Ts>
    void add(const std::tuple<Ts...>& t);

public:
    void ngrams(const std::vector<Trigram>& trigrams);
    void load(const std::string& corpus);
    void save(const std::string& path);

    size_t getSize();
    std::map<uint64_t, float> getCountsMap();
    Ngrams();

};

class SBModel {

private:
    const float ALPHA = 0.4;
    std::map<uint64_t, float> counts;
    size_t N;

    float __score(const Trigram& trigram, size_t n);

public:
    std::map<Trigram, float> score(const std::vector<Trigram>& trigrams);
    SBModel(const std::map<uint64_t, float>& counts, size_t N);

};


namespace fnv {

inline void fnv1_hash(const std::string& v, uint64_t* seed) {
    for (int i = 0; i < v.length(); i++) {
        *seed *= FNV_PRIME;
        *seed ^= v[i];
    }
}

inline void fnv1_hash(const unsigned& v, uint64_t* seed) {
    *seed *= FNV_PRIME;
    *seed ^= v;
}

template<unsigned index, typename... Ts>
struct tuple_hash {
    void operator() (const std::tuple<Ts...>& t, uint64_t* seed) {
        auto& item = std::get<index>(t);
        fnv1_hash(item, seed);
        tuple_hash<index - 1, Ts...>{}(t, seed);
    }
};

template<typename... Ts>
struct tuple_hash<0, Ts...> {
    void operator() (const std::tuple<Ts...>& t, uint64_t* seed) {
        auto& item = std::get<0>(t);
        fnv1_hash(item, seed);
    }
};

template<typename... Ts>
uint64_t hash(const std::tuple<Ts...>& t) {
    const size_t size = std::tuple_size<std::tuple<Ts...>>::value;
    uint64_t seed = FNV_OFFSET_BASIS;
    tuple_hash<size - 1, Ts...>{}(t, &seed);
    return seed;
};

}

template<size_t N, size_t... Ts>
constexpr std::index_sequence<N + Ts...>
add(std::index_sequence<Ts...>) {
    return {};
}

template<size_t L, size_t R>
using make_index_range = decltype(add<L>(std::make_index_sequence<R - L>()));

template <typename... T, size_t... I>
auto __slice(const std::tuple<T...>& t, std::index_sequence<I...>) {
    return std::make_tuple(std::get<I>(t)...);
}

template <int L, int R, typename... T>
auto slice(const std::tuple<T...>& t) {
    return __slice(t, make_index_range<L, R>());
}

template<typename... Ts>
void Ngrams::add(const std::tuple<Ts...>& t) {
    uint64_t hash = fnv::hash(t);
    if (counts.find(hash) == counts.end()) {
        counts[hash] = 1;
    } 
    else {
        ++counts[hash];
    }
}

void Ngrams::ngrams(const std::vector<Trigram>& trigrams) {
    for (auto& trigram : trigrams) {
        this->add(trigram);
        this->add(slice<0, 2>(trigram));
        this->add(slice<0, 1>(trigram));
    }
    size = trigrams.size();
}

size_t Ngrams::getSize() {
    return size;
}

std::map<uint64_t, float> Ngrams::getCountsMap() {
    return counts;
}

void Ngrams::load(const std::string& path) {
    std::ifstream in;
    std::ifstream _in;
    std::string _path;
    std::string temp;
    Logger::log("Loading binary data from: " + path);
    try {
        in.open(path, std::ios::in | std::ios::binary);
        while (!in.eof()) {
            std::pair<uint64_t, float> p;
            in.read((char*)&p.first, sizeof(uint64_t));
            in.read((char*)&p.second, sizeof(float));
            this->counts.insert(p);
        }
        // get total word count from file
        _path = path.substr(0, path.size() - 4) + "_size.txt";
        _in.open(_path);
        std::getline(_in, temp);
        this->size = std::stoi(temp);
    }
    catch (std::exception& e) {
        throw "no file found named: " + path;
    }
}

void Ngrams::save(const std::string& path) {
    std::ofstream os;
    std::ofstream _os;
    std::string _path;
    try {
        os.open(path, std::ios::out | std::ios::binary);
        for (auto& p : this->counts) {
            os.write((char*)&p.first, sizeof(uint64_t));
            os.write((char*)&p.second, sizeof(float));
        } 
        // save total word count to file
        _path = path.substr(0, path.size() - 4) + "_size.txt";
        _os.open(_path);
        _os << this->size;
    }
    catch (std::exception& e) {
        throw "no file found named: " + path;
    }
    Logger::log("ngrams have been persisted to binary .DAT file");
}

Ngrams::Ngrams() {
    Logger::log("Staring pybackoff...");
}


SBModel::SBModel(const std::map<uint64_t, float>& counts, size_t N) {
    this->counts = counts;
    this->N = N;
}

float SBModel::__score(const Trigram& trigram, size_t n) {
    if (n == 1) {
        uint64_t hash = fnv::hash(slice<2, 3>(trigram));
        return counts[hash] / (float)N;
    }
    if (n == 2) {
        uint64_t hash = fnv::hash(slice<1, 3>(trigram));
        if (counts[hash] > 0) {
            uint64_t hash1 = fnv::hash(slice<1, 2>(trigram));
            return counts[hash] / counts[hash1];
        }
        return ALPHA * this->__score(trigram, n - 1);
    }
    uint64_t hash = fnv::hash(trigram);
    if (counts[hash] > 0) {
        uint64_t hash1 = fnv::hash(slice<0, 2>(trigram));
        return counts[hash] / counts[hash1];
    }
    return ALPHA * this->__score(trigram, n - 1);

}

std::map<Trigram, float> SBModel::score(const std::vector<Trigram>& trigrams) {
    std::map<Trigram, float> scores;
    for (auto& trigram : trigrams) {
        scores[trigram] = this->__score(trigram, 3);
    }
    return scores;
}

////////////////////////////////////////////
/// PYBACKOFF PYTHON MODULE
////////////////////////////////////////////

PYBIND11_MODULE(pybackoff, m) {

    py::class_<Ngrams>(m, "Ngrams")
        .def(py::init<>())
        .def("ngrams", &Ngrams::ngrams, py::arg("trigrams"))
        .def("size", &Ngrams::getSize)
        .def("counts", &Ngrams::getCountsMap)
        .def("load", &Ngrams::load, py::arg("path"))
        .def("save", &Ngrams::save, py::arg("path"));

    py::class_<SBModel>(m, "SBModel")
        .def(py::init<const std::map<uint64_t, float>&, size_t>())
        .def("score", &SBModel::score, py::arg("trigrams"));

}
