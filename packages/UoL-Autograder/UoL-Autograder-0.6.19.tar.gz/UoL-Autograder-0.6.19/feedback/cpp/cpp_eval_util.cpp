#include "cpp_eval_util.h"

bool file_exists(string name){
    ifstream f(name.c_str());
    return f.good();
}

tuple<string, float> process_result(vector<string> result, vector<string> test_case, string question_specific_fail_message){
    int passed = 0;
    int failed = 0;
    int failed_error = 0;
    int count = result.size();

    for(int i = 0; i < count; i++){
        if(result[i] == "pass"){
            passed++;
        }
        else if(result[i] == "fail"){
            failed++;
        }
        else{
            failed_error++;
        }
    }

    string eval_feedback = "cpp_eval_feedback.json";
    if(!file_exists(eval_feedback)){
        cout << "FEEDBACK FILE MISSING!\n";
    }
    ifstream fb(eval_feedback.c_str());
    json func_feedback;
    fb >> func_feedback;

    string feedback = "";
    float score = 1;

    if(passed == count){
        feedback = func_feedback["pass"];
        return make_tuple(feedback, score);
    }
    else if(failed_error == 0) {
        feedback += func_feedback["fail"];
        if(question_specific_fail_message != "")
        {
            feedback += "\n" + question_specific_fail_message;
        }
        score = (float)passed / (float)count;
        return make_tuple(feedback, score);
    }
    else{
        feedback += "Failed with error!";
        score = (float)passed / (float)count;
        return make_tuple(feedback, score);
    }
}

bool is_within_margin(float a, float b, float margin){
    return abs(a - b) < margin;
}

bool is_within_margin(double a, double b, double margin){
    return abs(a - b) < margin;
}

void Results::add(std::string question, std::string score, float weight, std::string feedback)
{
    nlohmann::json test_case_result = {
        {"question", question},
        {"mark", score},
        {"weight", weight},
        {"feedback", feedback}
    };

    // add to test results vector
    _test_results.push_back(test_case_result);
}


void Results::output(char filename[])
{
    std::ofstream o(filename);
    nlohmann::json json_result = {_test_results};
    o << json_result[0].dump(4);
}

string byte_to_binary(int x)
{
    string b = "";
    for (int z = 128; z > 0; z >>= 1){ b += ((x & z) == z) ? "1" : "0"; }
    return b;
}

string vector_to_string(vector<int> a) {
    string r = "{";
    for(int i = 0; i < a.size(); i++){
        r += to_string(a[i]);
        if(i != a.size() - 1){
            r += ",";
        }
    }
    r += "}";
    return r;
}

string vector_to_string(vector<float> a) {
    string r = "{";
    for(int i = 0; i < a.size(); i++){
        r += to_string(a[i]);
        if(i != a.size() - 1){
            r += ",";
        }
    }
    r += "}";
    return r;
}
string vector_to_string(vector<double> a) {
    string r = "{";
    for(int i = 0; i < a.size(); i++){
        r += to_string(a[i]);
        if(i != a.size() - 1){
            r += ",";
        }
    }
    r += "}";
    return r;
}

string vector_to_string(vector<string> a) {
    string r = "{";
    for(int i = 0; i < a.size(); i++){
        r += "\"" + a[i] + "\"";
        if(i != a.size() - 1){
            r += ",";
        }
    }
    r += "}";
    return r;
}