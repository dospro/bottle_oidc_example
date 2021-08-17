<html>
<body>
<h1>Home page</h1>
<div>
%if name is not None:
  <p>Welcome to the home page {{name}}</p>
  <button><a href="logout">Log out</a></button>
%else:
  <p>You are not logged in</p>
  <button><a href="login">Log in</a></button>
%end
</div>
</body>
</html>