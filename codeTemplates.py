filenameReplaceTag = "FILE_NAME_TEMPLATE"

pyTemplate  = """with open('FILE_NAME_TEMPLATE') as f:
    lines = f.readlines()

for line in lines:
    print(line)

"""

cTemplate = """#include <stdio.h>

int main(int argc, char* argv[])
{
    char const* const fileName = "FILE_NAME_TEMPLATE";
    FILE* file = fopen(fileName, "r");
    char line[256];

    while (fgets(line, sizeof(line), file)) {
        printf("%s", line); 
    }

    fclose(file);

    return 0;
}

"""

rsTemplate = """use std::fs::File;
use std::io::{self, prelude::*, BufReader};

fn main() -> io::Result<()> {
    let file = File::open("FILE_NAME_TEMPLATE")?;
    let reader = BufReader::new(file);

    for line in reader.lines() {
        println!("{}", line?);
    }

    Ok(())
}


"""

cppTemplate = """#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

auto split_string(std::string full_string, char seperator) -> std::vector<std::string> {
    std::stringstream full_string_ss(full_string);
    std::vector<std::string> splitted_string;
    std::string split;

    while (std::getline(full_string_ss, split, seperator)) {
        if (split[0] == ' ') {
            split = split.substr(1, split.length() - 1);
        }
        splitted_string.push_back(split);
    }

    return splitted_string;
}

auto stringVec2intVec(std::vector<std::string>* vec_str) -> std::vector<int> {
    std::vector<int> vec_int;
    std::transform(vec_str->begin(), vec_str->end(), std::back_inserter(vec_int), [](const std::string& str) { return std::stoi(str); });
    return vec_int;
}

int main() {
    // std::ifstream file("input.txt");
    std::ifstream file("test.txt");
    std::string line;

    while (std::getline(file, line)) {
        std::cout << line << std::endl;
    }

    file.close();
    return 0;
}


"""

languageTemplates = {"py": pyTemplate, "c": cTemplate, "cpp": cppTemplate, "rs": rsTemplate}
