interface ButtonProps {
  value: string;
  onClick: () => void;
}

const LoginButton: React.FC<ButtonProps> = (props) => {
  return (
    <button
      className="bg-firebrick text-cultured text-2xl w-56 p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-imperialRed duration-200"
      onClick={props.onClick}
      type="submit"
      // onSubmit={props.onClick}
    >
      {props.value}
    </button>
  );
}

export default LoginButton;