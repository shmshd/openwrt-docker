FROM scratch

ARG VERSION="24.10.5"
ARG FILE_HOST="downloads.openwrt.org"
ARG FILE_NAME="openwrt-${VERSION}-x86-64-rootfs.tar.gz"

ENV VERSION=$VERSION
ENV USER=root

ADD --unpack=true "https://${FILE_HOST}/releases/${VERSION}/targets/x86/64/${FILE_NAME}" /

CMD ["/bin/ash"]

ENTRYPOINT ["/sbin/init"]
