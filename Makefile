# =====================

all: rpm

rpm:
	yum install -y rpm-build make gcc
	yum install -y openssl-devel readline-devel ncurses-devel autoconf kernel-headers tcp_wrappers-devel
	rpmbuild --define "_topdir ${PWD}" -ba SPECS/socat.spec

.PHONY: all
