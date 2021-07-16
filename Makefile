__default__:
	@echo "Please specify a target to make"

proto:
	python3 -m grpc_tools.protoc -Iprotobuf --python_out=protobuf --python_grpc_out=protobuf --grpc_python_out=protobuf protobuf/taskqueue/protobuf/service.proto
	python3 -m grpc_tools.protoc -Iexample --python_out=example --python_grpc_out=example example/cafe.proto

release-client:
	./scripts/release_check.sh
	cd client; python setup.py sdist --dist-dir ../dist

release-server:
	./scripts/release_check.sh
	cd server; python setup.py sdist --dist-dir ../dist

release-proto:
	./scripts/release_check.sh
	cd protobuf; python setup.py sdist --dist-dir ../dist

release: release-proto release-server release-client

setup.txt:
	pip-compile --index-url https://pypi.evo.dev/root/pypi/ --extra-index-url https://pypi.evo.dev/platform/pypi/ server/setup.py
