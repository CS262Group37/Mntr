const LoginButton = (props:any) => {
  const {
    value,
    onClick,
  } = props;

  return (
    <button
      className="bg-firebrick text-cultured text-2xl w-56 p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-imperialRed duration-200"
      onClick={onClick}
    >
      {value}
    </button>
  );
}

export default LoginButton;