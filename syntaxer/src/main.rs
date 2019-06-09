/*
 * @Author: Canopus (https://github.com/ParadoxZW)
 * @Date: 2019-05-30 22:06:02 
 * @Last Modified by: Canopus (https://github.com/ParadoxZW)
 * @Last Modified time: 2019-05-30 22:35:06
 */

use std::collections::HashMap;
use std::env;
use std::fs;

type TokenSet = Vec<String>;
// the data structure of syntax table
type Table = HashMap<String, HashMap<String, Box<TokenSet>>>;

fn map_constructor(text: String) -> Result<Table, ()> {
    let mut pros: Vec<TokenSet> = Vec::new();
    let mut map: Table = HashMap::new();
    for line in text.lines() {
        let mut c_iter = line.split_whitespace();
        let flag = c_iter.next();
        match flag {
            Some("#") => {
                let mut c_vec = c_iter.map(|x| x.to_string())
                                      .collect::<TokenSet>();
                pros.push(c_vec);  // record this production
            },
            Some("%") => {
                let row = c_iter.next().unwrap().to_string();
                let col = c_iter.next().unwrap().to_string();
                let idx = c_iter.next().unwrap().parse::<usize>().unwrap();
                map.entry(row.clone()).or_insert(HashMap::new());
                map.get_mut(&row).unwrap().insert(col, Box::new(pros.get(idx).unwrap().to_vec()));
            },
            _ => return Err(())
        }
    }
    Ok(map)
}

fn analyzer(mut input: TokenSet, 
            mut stack: TokenSet, 
            map: Table
            ) -> Result<i32, usize> {
    let mut top = stack.pop().unwrap();
    let mut flag = 0;
    while top != "$" {
        let token = input.pop().unwrap();
        if token != top {
            let key = map.get(&top)
                                .unwrap()
                                .get(&token);
            match key {
                Some(value) => {
                    let mut pro = value.clone();
                    print!("\n{}->", top);
                    for c in pro.iter() {
                        print!("{}", c);
                    }
                    if pro.get(0).unwrap() != &"ε" {
                        pro.reverse();
                        stack.append(&mut pro);
                    }
                },
                None => {
                    print!("\nerror token: {}", token);
                    flag = -1;
                }
            };
            input.push(token);
        } else {
            print!("\nmatch {}", token);
        }
        println!("\t{:?} {:?}", stack, input);
        top = stack.pop().unwrap();
    }
    Ok(flag)
}

fn main() {
    println!("Welcome to Syntax Analyzing Program");
    let args: TokenSet = env::args().collect();
    let gra_file = &args[1];
    let str_file = &args[2];

    println!("Loading grammar file '{}'...", gra_file);
    let gra_text = fs::read_to_string(gra_file)
        .expect("Something went wrong reading the file");

    let map = map_constructor(gra_text)
        .expect("There are syntax errors in grammar file");
    println!("LL(1) Table has bulit: {:?}", map);

    println!("loading token string file '{}'...", str_file);
    let contents = fs::read_to_string(str_file)
        .expect("Something went wrong reading the file");
    println!("Loading is finished.\nAnalyzing start...");

    let mut input: TokenSet = contents.split("")
                                         .filter(|x| (x != &""))
                                         .map(|x| x.to_string())
                                         .collect();
    input.push(format!("$"));
    input.reverse();
    let stack: TokenSet = vec![format!("$"), format!("E")];

    match analyzer(input, stack, map) {
        Ok(0) => {print!("\nThe token string is legal.");},
        _ => {print!("\nThe token string is illegal.");},
    };
    print!("\nSyntax analyzing has finished succesfully. Bye!");
}