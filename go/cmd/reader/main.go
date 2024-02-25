package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"time"
)

func readFile(filename string, startLineIdx int) ([]string, int) {

	file, err := os.Open(filename)
	if err != nil {
		panic(fmt.Errorf("Could not open file %v", filename))
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var lines []string
	idx := 0
	for scanner.Scan() {
		if idx >= *&startLineIdx {
			line := scanner.Text()
			lines = append(lines, line)
		}
		idx++

	}
	return lines, idx
}

func main() {
	inputFile := flag.String("input-file", "", "Input file, eg price.jsonl")
	frequency := flag.Int("frequency", 10, "Read every <frequency> seconds")
	start_line_idx := flag.Int("start-line-idx", 0, "Start reading from this idx line")

	flag.Parse()

	idx := *start_line_idx
	for {
		lines, idx := readFile(*inputFile, idx)
		fmt.Println(idx, lines[len(lines)-1])
		time.Sleep(time.Duration(*frequency) * time.Second)
	}

}
