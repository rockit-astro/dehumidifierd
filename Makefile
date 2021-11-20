RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

all:
	mkdir -p build
	${RPMBUILD} -ba clasp-dehumidifier-server.spec
	${RPMBUILD} -ba onemetre-dehumidifier-server.spec
	${RPMBUILD} -ba observatory-dehumidifier-client.spec
	${RPMBUILD} -ba python3-warwick-observatory-dehumidifier.spec
	mv build/noarch/*.rpm .
	rm -rf build
