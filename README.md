# Simple-UDP-Connection
A simple ready-to-use python script to communicate between any two computers via Internet

## How to use

### Basic usage

Initialize sender and receiver:

	# Sender:
	from udp_connection import UDPConnection
	udp = UDPConnection(TARGET_IP='127.0.0.1')

Alternative:

	# Sender:
	from udp_connection import UDPConnection
	udp = UDPConnection(TARGET_IP='yourcomputer')
	
Where you insert the receiver machine IP address to the `TARGET_IP`. Alternatively, you can use the hostname.

Initialize the receiver:

	# Receiver:
	from udp_connection import UDPConnection
	udp = UDPConnection(TARGET_IP='mycomputer')
	
You can also use the IP address as before.

Now you are ready to send the first message!
	
	# Sender:
	udp.send_message('Hello World')
	# send_message returns True upon success
	# In case of timeout or failure, the send_message returns False
To get the message, you query the buffer of the receiver computer:

	# Receiver:
	msg = udp.query_message() # waits until message arrives
	print msg
	# {'status': None, 'message': 'Hello Wolrd!'}
	
As you can see, the message is received as a dictionary that has the `message` as well as `status` keys. `message` contains the sent message and `status` is used to communicate the type of the message: confirmation, failure report or neutral message. All neutral messages will automatically be confirmed (you will know whether message was read or not). By default the confirmation has timeout of 10 seconds.

### Advanced features
You only need to know the address of one computer in order to establish two-way UDP communication. To do so, open the connection as before on the computer with unknown IP. On the receiving computer you don't give any parameters:
	
	# Receiver:
	udp = UDPConnection()
	
Then, you need to send an initialization message `'initialize'` to the receiver computer:

	# Sender
	udp.send_message('initialize')
	
Now, the receiver computer will capture the IP address from the incoming message and can now communicate back. You will be notified when the initialization has succeeded.

## Contribution and license
Use this as you wish (MIT license) in commercial or non-commercial projects. If you wish to advange this further with new features, create a pull request and share them with others!