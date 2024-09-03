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

cppTemplate = """#include <fstream>
#include <iostream>
#include <string>


int main(){
    std::ifstream file("input.txt");
    std::string line;

    while (std::getline(file, line)) {
        std::cout << line << std::endl;
    }



    file.close();
    return 0;
}

"""

languageTemplates = {"py": pyTemplate, "c": cTemplate, "cpp": cppTemplate, "rs": rsTemplate}
