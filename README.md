# Usage

## python digvuln.py <url>
example:
python digvuln.py http://192.168.1.1/

## login
example:
python digvuln.py http://192.168.1.1/ --login "id=aaa&password=bbb"

## stored XSS
example:
python digvuln.py http://192.168.1.1/ --store "http://192.168.1.1/sink.php" --login "name=aaa"
