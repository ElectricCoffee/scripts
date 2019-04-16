##
# Convenience function to deal with user prompts
# Prints +text+ to the terminal, then passes the user's response into the block
# +src+ is set to STDIN by default, but can be overridden if need be.
def prompt(text, src = STDIN)
    print text
    input = src.gets.chomp
    yield input
end
