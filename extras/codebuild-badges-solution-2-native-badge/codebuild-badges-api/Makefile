BUILD_DIR=build

all:
	mkdir -p $(BUILD_DIR)
	cp lambda_function.py $(BUILD_DIR)
	python -m pip install requests --target $(BUILD_DIR)
	cd $(BUILD_DIR) && zip -r9 ../function.zip .

clean:
	rm -Rf $(BUILD_DIR)
	rm function.zip
