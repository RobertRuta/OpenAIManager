from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='openai-api-manager',
    version='0.0.6',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    python_rqeuires='>=3.8',
    # metadata to display on PyPI
    author='Robert Ruta',
    author_email='robertruta50@gmail.com',
    description='This is a simple openAI API wrapper that makes it easier for me (and hopefully for you as well) to send messages via an assistant and manage threads locally with a custom thread key (such as message author) that is associated the thread id stored by open ai.',
    keywords=['OpenAI API', 'OpenAI Assistants', 'OpenAI Threads', 'ChatGPT', 'AI', 'Wrapper'],
    url='https://github.com/RobertRuta/OpenAIManager',  # project home page
    project_urls={
        'Source Code': 'https://github.com/RobertRuta/OpenAIManager',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    include_package_data=True
)
