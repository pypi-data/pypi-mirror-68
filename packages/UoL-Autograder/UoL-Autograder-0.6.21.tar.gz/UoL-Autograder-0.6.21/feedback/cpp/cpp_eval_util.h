#ifndef _CPP_EVAL_UTIL_H
#define _CPP_EVAL_UTIL_H

#include "json.hpp"
#include <vector>
#include <string>
#include <fstream>
#include <tuple>
#include <iostream>


using namespace std;
using namespace nlohmann;



tuple<string, float> process_result(vector<string> result, vector<string> test_case, string question_specific_fail_message = "");
bool is_within_margin(float a, float b, float margin);
bool is_within_margin(double a, double b, double margin);
string byte_to_binary(int x);
string vector_to_string(vector<int> a);
string vector_to_string(vector<float> a);
string vector_to_string(vector<double> a);
string vector_to_string(vector<string> a);

class Results
{
public:
   void add(std::string question, std::string score, float weight, std::string feedback);
   void output(char filename[]);

private:
   std::vector<nlohmann::json> _test_results;
};

#endif