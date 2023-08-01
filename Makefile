RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

all:
	mkdir -p build
	date --utc +%Y%m%d%H%M%S > VERSION
	${RPMBUILD} --define "_version %(cat VERSION)" -ba rockit-dehumidifier.spec
	${RPMBUILD} --define "_version %(cat VERSION)" -ba python3-rockit-dehumidifier.spec

	mv build/noarch/*.rpm .
	rm -rf build VERSION

install:
	@date --utc +%Y%m%d%H%M%S > VERSION
	@python3 -m build --outdir .
	@sudo pip3 install rockit.dehumidifier-$$(cat VERSION)-py3-none-any.whl
	@rm VERSION
	@cp dehumidifiered dehumidifier /bin/
	@cp dehumidifierd@.service /usr/lib/systemd/system/
	@cp completion/dehumidifier /etc/bash_completion.d/
	@install -d /etc/dehumidifierd
	@echo ""
	@echo "Installed server, client, and service files."
	@echo "Now copy the relevant json config file to /etc/dehumidifierd/"
