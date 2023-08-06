#include <vector>
#include "timeswipe.hpp"
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include "array_indexing_suite.h"
#include <iostream>

template <class T, class M> M get_member_type(M T:: *);
#define GET_TYPE_OF(mem) decltype(get_member_type(mem))

template <typename F>
auto GIL_WRAPPER(F&& f) {
    return [f=std::forward<F>(f)](auto&&... args) {
        auto gstate = PyGILState_Ensure();
        auto ret = f(std::forward<decltype(args)>(args)...);
        PyGILState_Release(gstate);
	return ret;
    };
}

BOOST_PYTHON_MODULE(timeswipe)
{
    using namespace boost::python;
    class_<SensorsData>("SensorsData")
        .def("SensorsSize",&SensorsData::SensorsSize,
                "Get sensors number")
        .def("DataSize",&SensorsData::DataSize,
                "Get data samples number")
        .def("sensor", +[](SensorsData& self, object obj) {
            int num = extract<int>(obj);
	    return self.data()[num];
        },
        "Get vector with data of corresponding sensor number [0..SensorsSize-1]")
    ;
    class_<std::vector<float>>("SensorData")
        .def(vector_indexing_suite<std::vector<float>>());


    class_<TimeSwipe, boost::noncopyable>("TimeSwipe")
        .def("SetMode", +[](TimeSwipe& self, object object) {
                std::string mode = extract<std::string>(object);
                    TimeSwipe::Mode m;
                    if (mode == "PRIMARY") {
                        m = TimeSwipe::Mode::Primary;
                    } else if (mode == "NORM") {
                        m = TimeSwipe::Mode::Norm;
                    } else if (mode == "DIGITAL") {
                        m = TimeSwipe::Mode::Digital;
                    } else {
                        return false;
                    }
                    self.SetMode(m);
                    return true;
                },
               "Setup hardware mode")
        .def("GetMode", +[](TimeSwipe& self, object object) {
                    auto m = self.GetMode();
                    if (m == TimeSwipe::Mode::Primary) {
                        return "PRIMARY";
                    } else if (m == TimeSwipe::Mode::Norm) {
                        return "NORM";
                    } else if (m == TimeSwipe::Mode::Digital) {
                        return "DIGITAL";
                    }
                    return "";
                },
               "Get current hardware mode")
        .def("SetSensorOffsets", &TimeSwipe::SetSensorOffsets,
               "Setup Sensor offsets. It is mandatory to setup offsets before Start" )
        .def("SetSensorGains", &TimeSwipe::SetSensorGains,
                "Setup Sensor gains. It is mandatory to setup gains before Start")
        .def("SetSensorTransmissions", &TimeSwipe::SetSensorTransmissions,
                "Setup Sensor transmissions. It is mandatory to setup transmissions before Start")
        .def("StartPWM", &TimeSwipe::StartPWM,
                "Start PWM generator")
        .def("StopPWM", &TimeSwipe::StopPWM,
                "Stop PWM generator")
        .def("GetPWM", +[](TimeSwipe& self, object object) {
                    bool active;
                    uint32_t frequency;
                    uint32_t high;
                    uint32_t low;
                    uint32_t repeats;
                    float duty_cycle;
                    auto num = extract<int>(object);
                    auto ret = self.GetPWM(num, active, frequency, high, low, repeats, duty_cycle);
                    return make_tuple(ret, active, frequency, high, low, repeats, duty_cycle);
                },
                "Get PWM generator state if it is in a Start state. Returns tuple (result, active, frequency, high, low, repeats, duty_cycle)")
        .def("SetBurstSize", &TimeSwipe::SetBurstSize,
                "Setup burst buffer size")
        .def("SetSampleRate", &TimeSwipe::SetSampleRate,
                "Setup sample rate. Default value is 48000")
        .def("Start", +[](TimeSwipe& self, object object) {
            try {
                    SensorsData records;
                    uint64_t errors = 0;
                    GIL_WRAPPER(object)(records, errors);
            }
            catch (const error_already_set&)
            {
                PyErr_Print();
                return false;
            }

            return self.Start(GIL_WRAPPER(object));
        },
            "Start reading Sensor loop. It is mandatory to setup SetBridge SetSensorOffsets SetSensorGains and SetSensorTransmissions before start. Only one instance of TimeSwipe can be running each moment of the time. After each sensor read complete cb called with SensorsData. Buffer is for 1 second data if cb works longer than 1 second, next data can be loosed and next callback called with non-zero errors")
        .def("SetSettings", +[](TimeSwipe& self, object object) {
                std::string error;
                std::string in = extract<std::string>(object);
                auto ret = self.SetSettings(in, error);
                return error;
            }
            ,"Send SPI SetSettings request and receive the answer. Returns error_message")
        .def("GetSettings", +[](TimeSwipe& self, object object) {
                std::string error;
                std::string in = extract<std::string>(object);
                auto ret = self.GetSettings(in, error);
                return error;
            }
             ,"Send SPI GetSettings request and receive the answer. Returns error_message")
        .def("onEvent", +[](TimeSwipe& self, object object) {
                self.onEvent([object=GIL_WRAPPER(object)] (TimeSwipeEvent&& ev) {
                    static auto* arr_ptr = new dict;
                    auto& arr = *arr_ptr;
                    arr.clear();
                    if (ev.is<TimeSwipeEvent::Button>()) {
                        const auto& button = ev.get<TimeSwipeEvent::Button>();
                        arr["type"] = "Button";
                        arr["pressed"] = button.pressed();
                        arr["count"] = button.count();
                    } else if (ev.is<TimeSwipeEvent::Gain>()) {
                        arr["type"] = "Gain";
                        arr["value"] = ev.get<TimeSwipeEvent::Gain>().value();
                    } else if (ev.is<TimeSwipeEvent::SetSecondary>()) {
                        arr["type"] = "SetSecondary";
                        arr["value"] = ev.get<TimeSwipeEvent::SetSecondary>().value();
                    } else if (ev.is<TimeSwipeEvent::Bridge>()) {
                        arr["type"] = "Bridge";
                        arr["value"] = ev.get<TimeSwipeEvent::Bridge>().value();
                    } else if (ev.is<TimeSwipeEvent::Record>()) {
                        arr["type"] = "Record";
                        arr["value"] = ev.get<TimeSwipeEvent::Record>().value();
                    } else if (ev.is<TimeSwipeEvent::Offset>()) {
                        arr["type"] = "Offset";
                        arr["value"] = ev.get<TimeSwipeEvent::Offset>().value();
                    } else if (ev.is<TimeSwipeEvent::Mode>()) {
                        arr["type"] = "Mode";
                        arr["value"] = ev.get<TimeSwipeEvent::Mode>().value();
                    } else {
                        arr["type"] = "UNKNOWN";
                    }

                    GIL_WRAPPER(object)(arr);
                });
        },
            "Register callback for button pressed/released. onButton must be called before called, otherwise register fails")
        .def("onError", +[](TimeSwipe& self, object object) {
            self.onError(GIL_WRAPPER(object));
        },
            "onError must be called before Start called, otherwise register fails")
        .def("Stop", &TimeSwipe::Stop,
            "Stop reading Sensor loop")
        .def("TraceSPI", &TimeSwipe::TraceSPI,
            "Trace SPI")
    ;
}

