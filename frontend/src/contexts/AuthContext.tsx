import React, { createContext, useState, useEffect } from "react";
import jwt_decode from "jwt-decode";

// The attributes of decoded token
export type DecodedToken = {
  id: number;
  is_librarian: boolean;
  sub: string;
  isAuthenticated: boolean;
};

export interface DecodedRefreshToken {
  token_type: string;
  exp: number;
  jti: string;
  id: number;
  isLibrarian: boolean;
  sub: string;
}

// The attributes in context
type ContextAttributes = {
  user_id: number;
  isLibrarian: boolean;
  isAuthenticated: boolean;
  username: string;
  LoginFunction: (arg0: DecodedToken) => void;
  LogoutFunction: () => void;
};

const default_value: ContextAttributes = {
  user_id: -1,
  username: "",
  isLibrarian: false,
  isAuthenticated: false,
  LoginFunction: (default_value: DecodedToken) => {},
  LogoutFunction: () => {},
};

export const AuthContext = createContext<ContextAttributes>({
  ...default_value,
});

function AuthContextProvider({ children }: { children: JSX.Element[] }) {
  /**
   * This context is where we store the state details as they pertain to the current user
   */
  const [isAuthenticated, setIsAuthenticated]: [
    boolean,
    React.Dispatch<React.SetStateAction<boolean>>
  ] = useState<boolean>(false); //This is used for components that only render based on whether a user is logged in or not i.e the login/logout component
  const [user_id, setUserId]: [
    number,
    React.Dispatch<React.SetStateAction<number>>
  ] = useState(-1); //This is used in case we need to use the current users id for any future api call or rendering i.e to check the books borrowed by the current user
  const [username, setUsername]: [
    string,
    React.Dispatch<React.SetStateAction<string>>
  ] = useState("");
  const [isLibrarian, setIsLibrarian]: [
    boolean,
    React.Dispatch<React.SetStateAction<boolean>>
  ] = useState<boolean>(false); //This is used to render components based on whether or not the user has librarian credentials or not. a user can do create, update or delete operations

  useEffect(() => {
    const tok = localStorage.getItem("access_token");

    if (tok != null) {
      const decoded_tok: DecodedToken = jwt_decode(tok);

      setIsAuthenticated(true);
      setUserId(decoded_tok.id);
      setIsLibrarian(decoded_tok.is_librarian);
      setUsername(decoded_tok.sub);
    } else {
      setIsAuthenticated(false);
      setUserId(-1);
      setIsLibrarian(false);
      setUsername("");
    }
  }, []);

  //This function is called when a user successfully logs in
  const LoginFunction = (access_token: DecodedToken) => {
    setIsAuthenticated(true);
    setUserId(access_token.id);
    setIsLibrarian(access_token.is_librarian);
    setUsername(access_token.sub);
  };

  //This is called when a user logs out
  const LogoutFunction = () => {
    setIsAuthenticated(false);
    setUserId(-1);
    setIsLibrarian(false);
    setUsername("");
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user_id,
        isLibrarian,
        username,
        LoginFunction: LoginFunction,
        LogoutFunction: LogoutFunction,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthContextProvider;
