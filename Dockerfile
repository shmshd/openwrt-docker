FROM scratch

ARG VERSION

ENV VERSION=$VERSION
ENV USER=root

ADD --unpack=true "https://downloads.openwrt.org/releases/${VERSION}/targets/x86/64/openwrt-${VERSION}-x86-64-rootfs.tar.gz" /

CMD ["/bin/ash"]

ENTRYPOINT ["/sbin/init"]
