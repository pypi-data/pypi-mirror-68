#!/bin/bash

# This is the old Bash version. It is no longer updated and is now superceded
# by the Python version.

print_help() {
  printf 'Telegram HTTP notification script, version 0.0.1\n'
  printf "Usage: %s [option] ...\\n" "${0}"
  printf '\n'
  printf '  -c, --chat-id         override the Telegram chat ID to post to\n'
  printf '  -h, --help            display this help and exit\n'
  printf '  -g, --geo             include geographical information\n'
  printf '  -i, --ignore-ips      ignore (multiple) IP addresses (e.g. 127.0.0.1,::1)\n'
  printf '  -k, --bot-key         override the Telegram bot key\n'
  printf '  -l, --log-file        override the Nginx log file\n'
  printf '  -m, --map             post a separate map pointer\n'
  printf '  -r, --match-requests  match (multiple) specific HTTP requests (e.g. /,/robots.txt)\n'
  printf '  -s, --silent          send Telegram messages silently\n'
  printf '  -u, --user-agent      include the user agent string\n'
  printf '\n'
  exit 0
}

get_args() {
  while [[ "$1" ]]; do
    case "$1" in
      -c|--chat-id) TELEGRAM_CHAT_ID="${2}" ;;
      -h|--help) print_help ;;
      -g|--geo) GET_LOCATION=1 ;;
      -i|--ignore-ips) string_to_array "${2}" IGNORE ;;
      -k|--bot-key) TELEGRAM_BOT_KEY="${2}" ;;
      -l|--log-file) NGINX_LOG_FILE="${2}" ;;
      -m|--show-map) GET_LOCATION=1 MAP_POINTER=1 ;;
      -r|--match-requests) ENABLE_MATCH_DOCUMENTS=1 string_to_array "${2}" MATCH_DOCUMENTS ;;
      -s|--silent) SILENT=1 ;;
      -u|--user-agent) POST_UA=1 ;;
    esac
    shift
  done
}

get_vars() {
  # Uncomment to hardcode your Ngninx access.log file
  #NGINX_LOG_FILE="/var/log/nginx/access.log"

  # Uncomment to hardcode your Telegram private chat ID
  #TELEGRAM_CHAT_ID="-1234567890123"

  # Uncomment to harcode your Telegram bot key
  #TELEGRAM_BOT_KEY="123456789:1234567890abcdefghijklmnopqrstuvwxyz"

  # The Telegram API end point, which needs a bot key
  TELEGRAM_API="https://api.telegram.org/bot${TELEGRAM_BOT_KEY}"

  # Uncomment to only match the following hardcoded documents
  #MATCH_DOCUMENTS=(
  #  /
  #  /robots.txt
  #)

  # Uncomment to ignore the following IPs
  #IGNORE=(
  #  127.0.0.1
  #  ::1
  #)
}

string_to_array() {
  local IFS=','
  read -r -a "${2}" <<< "${1}"
}

contains_element () {
  local ELEMENT MATCH="${1}"
  shift
  for ELEMENT; do
    if [[ "${ELEMENT}" == "${MATCH}" ]] ; then
      return 0
    fi
  done
  return 1
}

main() {
  tail -n 1 -f "${NGINX_LOG_FILE}" | while read -r LINE ; do

    # Get the originating IP from each new line of the access.log file
    SRC_ADDR="$(printf "%s" "${LINE}" | awk '{print $1}')"
    REQUEST="$(printf "%s" "${LINE}" | awk -F\" '{print $2}' | sed 's| HTTP/.*||')"
    HTTP_CODE="$(printf "%s" "${LINE}" | awk -F \" '{print $3}' | awk '{print $1}')"
    UA="$(printf "%s" "${LINE}" | awk -F\" '{print $6}')"

    # If SRC_ADDR is not in IGNORE (our list of ignored IP addresses), then proceed
    if ! contains_element "${SRC_ADDR}" "${IGNORE[@]}" ; then

      # If client requests any document (in MATCH_DOCUMENTS), then proceed
      if contains_element "${REQUEST}" "${MATCH_DOCUMENTS[@]}" || [ -z "${MATCH_DOCUMENTS[1]}" ] ; then

        # If GET_LOCATION, get location stuff first
        if [[ "${GET_LOCATION}" == 1 ]] ; then
          WHOIS="$(curl -s "ipinfo.io/${SRC_ADDR}")"
          COUNTRY="$(printf "%s" "${WHOIS}" | jq ".country" | tr -d "\"" | cut -d "," -f 1)"
          REGION="$(printf "%s" "${WHOIS}" | jq ".region" | tr -d "\"" | cut -d "," -f 1)"
          CITY="$(printf "%s" "${WHOIS}" | jq ".city" | tr -d "\"" | cut -d "," -f 1)"
          ORG="$(printf "%s" "${WHOIS}" | jq ".org" | tr -d "\"" | cut -d "," -f 1)"
          LATITUDE="$(printf "%s" "${WHOIS}" | jq ".loc" | tr -d "\"" | cut -d "," -f 1)"
          LONGITUDE="$(printf "%s" "${WHOIS}" | jq ".loc" | tr -d "\"" | cut -d "," -f 2)"
	  CLIENT="${SRC_ADDR} (${COUNTRY}, ${REGION}, ${CITY}, ${ORG})"
        else
          CLIENT="${SRC_ADDR}"
        fi

        # If POST_UA, set USER_AGENT
        if [[ "${POST_UA}" == 1 ]] ; then
          USER_AGENT=", using ${UA}"
        fi

        # Post message
        curl \
          -s \
          -X POST \
          -H 'Content-Type: application/json' \
          -d "
            {
              \"chat_id\": \"${TELEGRAM_CHAT_ID}\",
              \"text\": \"${CLIENT} requested ${REQUEST} (${HTTP_CODE})${USER_AGENT}\",
	      \"disable_web_page_preview\": true,
              \"disable_notification\": ${SILENT}
            }" \
          "${TELEGRAM_API}"/sendMessage | jq

        # If GET_LOCATION and MAP_POINTER, post location on the map as well
        if [[ "${GET_LOCATION}" == 1 ]] && [[ "${MAP_POINTER}" == 1 ]] ; then
          curl \
            -s \
            -X POST \
            -H 'Content-Type: application/json' \
            -d "
              {
                \"chat_id\": \"${TELEGRAM_CHAT_ID}\",
                \"latitude\": \"${LATITUDE}\",
                \"longitude\": \"${LONGITUDE}\",
		\"disable_notification\": ${SILENT}
              }" \
            "${TELEGRAM_API}"/sendLocation | jq
        fi
      fi
    fi
  done
}

get_args "$@"
get_vars
main
