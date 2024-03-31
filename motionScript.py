class MotionScriptInterpreter:
    def __init__(self):
        self.memory = [0] * 10
        self.pointer = 0
        self.instruction_pointer = 0
        self.input_buffer = ''
        self.output_buffer = ''

    def get_prointer(self):
        len_up_to_pointer = len(" ".join([str(x) for x in self.memory[:self.pointer]]))
        if len_up_to_pointer > 0:
            len_up_to_pointer+=1
        return " "*len_up_to_pointer + "^"

    # def get_pointer_x(self):
    #     len_up_to_pointer = len(" ".join([str(x) for x in self.memory[:self.pointer]]))
    #     return len_up_to_pointer * 40 + 20

    def get_memory(self):
        return " ".join([str(x) for x in self.memory])

    def interpret(self, code, input_str=''):
        print("Code:", code)
        print("memory:", self.get_memory())
        # self.input_buffer = input_str
        # self.output_buffer = ''
        # self.memory = [0] * 10
        # self.pointer = 0
        self.instruction_pointer = 0

        while self.instruction_pointer < len(code):
            instruction = code[self.instruction_pointer]

            if instruction == '>':
                self.pointer += 1
            elif instruction == '<':
                self.pointer -= 1
            elif instruction == '+':
                self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256
            elif instruction == '-':
                self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256
            elif instruction == '.':
                # make 1-26 a-z
                if self.memory[self.pointer] == 0:
                    self.output_buffer += " "
                if self.memory[self.pointer] <= 26:
                    self.output_buffer += chr(self.memory[self.pointer]+ 96)
                else: # make 27-52 A-Z
                    self.output_buffer += chr(self.memory[self.pointer]+38)
                
            elif instruction == ',':
                if self.input_buffer:
                    self.memory[self.pointer] = ord(self.input_buffer[0])
                    self.input_buffer = self.input_buffer[1:]
                else:
                    self.memory[self.pointer] = 0
            elif instruction == '[':
                if self.memory[self.pointer] == 0:
                    bracket_count = 1
                    while bracket_count != 0:
                        self.instruction_pointer += 1
                        if code[self.instruction_pointer] == '[':
                            bracket_count += 1
                        elif code[self.instruction_pointer] == ']':
                            bracket_count -= 1
            elif instruction == ']':
                if self.memory[self.pointer] != 0:
                    bracket_count = 1
                    while bracket_count != 0:
                        self.instruction_pointer -= 1
                        if code[self.instruction_pointer] == ']':
                            bracket_count += 1
                        elif code[self.instruction_pointer] == '[':
                            bracket_count -= 1

            self.instruction_pointer += 1

        print("Output:", self.output_buffer)
        print("-"*len(self.get_memory()))
        return self.output_buffer


# Example usage:
if __name__ == "__main__":
    interpreter = MotionScriptInterpreter()
    code = "++++[>+++++++++++++<-]>."
    output = interpreter.interpret(code)
    print("Output:", output)
