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
   void set(int i, std::string question, std::string score, float weight, std::string feedback);
   void output(char filename[]);

private:
   std::vector<nlohmann::json> _test_results;
};

template<class T>
class Evaluator
{
  public:
    Evaluator(int n, int skip=0) : _n(n), _skip(skip) { }

    virtual string GetName(int i) = 0;
    virtual T GetResult(int i) = 0;
    virtual float GetScore(int i, T result) = 0;
    virtual string GetFeedback(int i, T result, float score) = 0;

    void Run(char* filename){
      for(int i = 0; i < _n; i++){
         _results.add(GetName(i), "", 1.0/_n, "");
      }

      string feedback = "";
      float score = 0;
      for(int i = _skip; i < _n; i++){
         printf("%d\n", i);
        try{
          T result = GetResult(i);
          score = GetScore(i, result);
          feedback = GetFeedback(i, result, score);
        }
        catch (exception& e)
        {
          feedback = "An error occured:\n";
          feedback += e.what();
          feedback += "\n : FAIL!";
        }
        _results.set(
           i,
          GetName(i),
          to_string(score),
          1.0/_n,
          feedback);
         _results.output(filename);
      }
      _results.output(filename);
    }

  private:
    int _n;
    int _skip;
    Results _results;
};

#endif