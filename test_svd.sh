#!/bin/bash

CHIPS=(rp2040 XMC4700)

do_test() {
	rm -rf build/svd
	mkdir -p build/svd && pushd build/svd || exit

	PKG=ifgen
	IG=../../venv/bin/ig

	for CHIP in "${CHIPS[@]}"; do
		mkdir -p "$CHIP/$PKG"
		$IG svd -o "$CHIP/$PKG" "package://$PKG/svd/$CHIP.svd" &
		ENTRY="$CHIP/$PKG.yaml"
		echo "---" > "$ENTRY"
		echo "includes:" >> "$ENTRY"
		echo "  - $PKG/$PKG.yaml" >> "$ENTRY"
	done
	wait

	for CHIP in "${CHIPS[@]}"; do
		$IG -C "$CHIP" gen &
	done
	wait

	popd >/dev/null || exit
}

time do_test
