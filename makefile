all:
	php test.php --int-only --directory=ipp-2023-tests/interpret-only/frames --recursive > out.html

my:
	php mytest.php interpret-only/32

every:
	php mytest.php interpret-only/

this:
	python3 interpret.py --source=ipp-2023-tests/interpret-only/valid/label_call_return.src --input=ipp-2023-tests/interpret-only/valid/label_call_return.in