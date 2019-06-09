/*
 * @Author: Canopus (https://github.com/ParadoxZW)
 * @Date: 2019-04-07 16:31:32 
 * @Last Modified by: Canopus (https://github.com/ParadoxZW)
 * @Last Modified time: 2019-04-07 17:27:39
 */
use std::env;
use std::fs;
extern crate rayon;
extern crate regex;
use regex::Regex;
use rayon::prelude::*;

#[derive(Debug)]
struct DFA(i32);

impl DFA {
    fn transaction(&mut self, c: &char) {
        match (self.0, c) {
            (0, '0'..='9') => self.0 = 1,
            (0, 'a'..='z')|(0, 'A'..='Z') => self.0 = 2,
            (2, '0'..='9') => self.0 = 2,
            (2, 'a'..='z')|(1, 'A'..='Z') => self.0 = 2,
            (1, '0'..='9') => self.0 = 1,
            _ => self.0 = 3  // mark syntax error 
        }
    }
}

fn sub_analyzer(s: &str) -> i16 {
    let dfa = &mut DFA(0);
    for c in s.chars() {
        if dfa.0 == 3 {
            break;
        }
        dfa.transaction(&c);
    }
    match dfa.0 {
        1 => 11,
        2 => 10,
        _ => -1
    }
}

fn analyzer(s: &str) -> i16 {
    match s {
        "begin" => 1,
        "if" => 2,
        "then" => 3,
        "while" => 4,
        "do" => 5,
        "end" => 6,
        "+" => 13,
        "-" => 14,
        "*" => 15,
        "/" => 16,
        ":" => 17,
        ":=" => 18,
        "<" => 20,
        "<>" => 21,
        "<=" => 22,
        ">" => 23,
        ">=" => 24,
        "=" => 25,
        ";" => 26,
        "(" => 27,
        ")" => 28,
        "#" => 0,
        _ => sub_analyzer(s),
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    println!("Loading {}...", filename);
    let contents = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");
    println!("Loading is finished.\nAnalyzing start...");

    // split all words by insert whitespaces between operaters and expressions
    let re = Regex::new(r"(\+|-|\*|/|:=|:|<>|<|<=|>|>=|=|;|\(|\)|#)").unwrap();
    let contents = re.replace_all(&contents, " $1 ");

    let words: Vec<&str> = contents
                        .split_whitespace()
                        .collect();    
    let ret:Vec<(i16, &str)> = words.par_iter()
                        .map(|&s| (analyzer(s), s))
                        .collect();  // process parallely    
    println!("Analyzing is finished!\nPrint the result of lexical analyzing:");
    for tup in ret {
        if tup.0 != -1 {
            println!("({}, {})", tup.0, tup.1);
        }else {
            println!("Error word: {}", tup.1);
        }
    } 
    println!("This program is finished. Bye!");
}