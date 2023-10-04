#!/bin/bash

mkdir >/dev/null -p build

pushd build || exit

for CHIP in rp2040 XMC4700; do
	../venv/bin/ig svd -o $CHIP package://ifgen/svd/$CHIP.svd &
done

wait

popd >/dev/null || exit
