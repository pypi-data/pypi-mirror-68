import sys
import os
    
def kbox_execute():   
    JAR_EXECUTE = "java -jar kbox.jar" # kbox-v0.0.2-alpha.jar

    if(len(sys.argv) ==1 ):
        returned_output = os.system(JAR_EXECUTE)
    else:
        arg = " ".join(sys.argv[1:])
        execute = JAR_EXECUTE + " " + arg 
        returned_output = os.system(execute)


if __name__ == "__main__":
    kbox_execute()
