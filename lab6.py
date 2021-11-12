from led8x8 import LED8x8
import multiprocessing as mp
import time
import RPi.GPIO as gpio
from random import randint
import sys

# pin numbers
data_pin = 26
latch_pin = 22
clock_pin = 21

# smilie face :)
def smile():
    pattern = [0b00111100,
               0b01000010,
               0b10100101,
               0b10000001,
               0b10100101,
               0b10011001,
               0b01000010,
               0b00111100]

    try:
        led_board = LED8x8(data_pin, latch_pin, clock_pin)
        led_board.display(pattern)
    except KeyboardInterrupt:
        print('Exiting\n')
    except Exception as e:
        print(f'Exiting because: {e}\n')
    finally:
        gpio.cleanup()
        sys.exit()


# firefly
def firefly():
    # intialize shared array
    pattern = mp.Array('i', 8) # 8 bytes of data using int datatype
    # intialize random position
    row, col = randint(0, 7), randint(0, 7)
    # encode position into pattern array
    pattern[row] = 128 >> col # 128 = 0b10000000
    # main
    try:
        # create our led board object
        led_board = LED8x8(data_pin, latch_pin, clock_pin)
        # target our display method in our process
        # the shared array is the argument for display
        proc = mp.Process(target=led_board.display, args=(pattern,))
        # terminate at the end of main
        proc.daemon = True
        # get this party rollin!
        proc.start()
        # this while loop is responcible for updating the position of
        # the firefly every 0.1s
        while 1:
            # update row first
            # get a random direction for the row to go in
            x = randint(-1, 1)
            if x: # do nothing if x is 0
                # making use of error handling to simplfy things
                # error handling minimizes the number of logical statements
                try:
                    pattern[row + x] # will throw an exception if row + x is
                                     # out of index range
                    if row + x < 0:
                        raise IndexError('Come back and simplify this')
                except IndexError:
                    pass # do nothing exactly as planned
                else:
                    # if no errors are raised then we update the pattern array
                    pattern[row] = 0
                    row += x

            # update col
            # generate another random direction
            x = randint(-1, 1)
            # if x is zero nothing happens
            if x < 0 and col > 0: # avoids moving the bit out of range
                col -= 1
            elif x > 0 and col < 7:
                col += 1

            # update the pattern so our firefly is on fire
            pattern[row] = 128 >> col
            # he takes his time
            time.sleep(0.1)

    except KeyboardInterrupt:
        print('Exiting\n')
    except Exception as e:
        print(f'Exiting because: {e}\n')
    finally:
        gpio.cleanup()
        proc.terminate()
        proc.join(2)

# runtime
if len(sys.argv) > 1 and sys.argv[1] == '--smile': # avoids error by evaluating length first
    smile()
else:
    firefly()
