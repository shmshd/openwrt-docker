FROM scratch

ARG VERSION="24.10.5"
ARG CMD=/bin/ash
ARG USER=root
ARG FILE_HOST="downloads.openwrt.org"
ARG FILE_NAME="openwrt-${VERSION}-x86-64-rootfs.tar.gz"

ENV CMD=$CMD
ENV USER=$USER
ENV VERSION=$VERSION

ADD --unpack=true "https://${FILE_HOST}/releases/${VERSION}/targets/x86/64/${FILE_NAME}" /

ENV CMD_ENV=${CMD}
CMD ${CMD_ENV}

ENTRYPOINT ["/sbin/init"]
