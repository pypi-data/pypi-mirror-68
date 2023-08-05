from setuptools import setup

setup(
    name='voice-transcriber-client',
    version='1.0.0',
    description='A python client for the https://github.com/jamesridgway/voice-transcriber project.',
    long_description=open('README.md').read(),
    author='James Ridgway',
    author_email='james@jamesridgway.co.uk',
    url='https://github.com/jamesridgway/voice-transcriber-client',
    license='MIT',
    packages=['voice_transcriber'],
    scripts=['bin/voice-transcriber'],
    install_requires=["pyperclip", "requests"]
)
