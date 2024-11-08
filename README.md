# Angler
<h3>Introduction</h3>
<p>
  Give a researcher Python code and you feed him for a day. <br>
  Give a researcher Angler, and you feed him until he needs something that isn't implemented yet. <br>
  In that case, your job as a Python developer will be less redundant anyway. 
</p>
<p>
  Angler is a domain specific language for research. It was designed for teams with researchers and programmers. 
  It works as a simple, high level language that can be easily used by researchers, and easily updated by programmers 
  to meet the specific needs of their coworkers. 
</p>
<p>
  The idea behind this approach is that data for research is too unpredictable for a DSL to encompass all applications, but
  general purpose programming languages require too much time to learn. Instead, Angler is designed to be updated by programmers
  so they don't need to constantly write programs for researchers that do the same thing. 
</p>
  
<h3>Capabilities</h3>
<h4>Manipulate data on your terminal</h4>
<img src="https://github.com/user-attachments/assets/410c92e6-d57b-4a6c-91a4-716042ee2e3a">
<p></p>
<h4>Or write programs in text files</h4>
<img src="https://github.com/user-attachments/assets/f0a93410-7d31-4ae3-a3e2-a0410cfd4874">

<p>The above code produces the following result:</p>
<img src="https://github.com/user-attachments/assets/06571d78-e0d3-47ea-a505-14cd213f8ff2">

<h3>How it works</h3>
<p>
  There are two types of programmer defined objects in Angler:
  <ul>
    <li>
      Structures: Include all data like files, lists, tables, text, and numbers. Each structure has
      operations that can be performed on it. The default operations in Angler are Print, Filter, Remove, Replace, and Count. 
    </li>
    <li>
      Predicates: Check if a condition is met. Predicates are used as arguments for some operations. For example, in the
      terminal demo above, the predicate "ByMinValueAtCol" is used by the Filter operation to determine which records should be kept. 
    </li>
  </ul>
</p>

<p>
  To ensure that Angler is easy to update, it is written in Python. As seen below, Angler usese a regex lexer to tokenize programs,
  a parser to create syntax trees, and an interpreter to run programs. 
</p>
<img src="https://github.com/user-attachments/assets/6f1048ce-7a07-4bf5-a2b5-fdb5cade1ea2">
