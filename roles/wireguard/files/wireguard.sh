#!/bin/sh

# PROVIDE: wireguard
# REQUIRE: LOGIN
# BEFORE:  securelevel
# KEYWORD: shutdown

. /etc/rc.subr

name="wg"
rcvar=wg_enable

command="/usr/local/bin/wg-quick"
start_cmd=wg_up
stop_cmd=wg_down
status_cmd=wg_status
pidfile="/var/run/$name.pid"
load_rc_config "$name"

: ${wg_enable="NO"}
: ${wg_interface="wg0"}

wg_up() {
  echo "Authenticating user for WireGuard..."
  
  # Execute the MongoDB authentication Python script
  python3 /home/abhishek/algo/library/mongo_authenticate.py
  if [ $? -ne 0 ]; then
      echo "Authentication failed. WireGuard setup aborted."
      exit 1
  fi

  echo "Initializing MongoDB table for WireGuard..."
  
  # Execute the MongoDB table creation Python script
  python3 /home/abhishek/algo/library/mongo_create_table.py
  if [ $? -ne 0 ]; then
      echo "MongoDB table creation failed. WireGuard setup aborted."
      exit 1
  fi

  echo "Starting WireGuard..."

  python3 /home/abhishek/algo/library/update_wiregaurd_config.py
  if [ $? -ne 0 ]; then
     echo "update the public keys "
     exit 1
  fi

  echo "update the public keys "

  # Start WireGuard using daemon for background operation
  /usr/sbin/daemon -cS -p ${pidfile} ${command} up ${wg_interface}
  if [ $? -eq 0 ]; then
      echo "WireGuard started successfully."
  else
      echo "Failed to start WireGuard."
      exit 1
  fi
}

wg_down() {
  echo "Stopping WireGuard..."
  ${command} down ${wg_interface}
}

wg_status () {
  not_running () {
    echo "WireGuard is not running on $wg_interface" && exit 1
  }
  /usr/local/bin/wg show wg0 && echo "WireGuard is running on $wg_interface" || not_running
}

run_rc_command "$1"
