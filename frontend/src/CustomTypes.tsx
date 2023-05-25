/**
 * This file contains custom data types and interfaces that are generic enough to be used multiple times throughout the project
 */

export interface AuthorDetails {
  first_name?: string | null;
  last_name?: string | null;
  birth_date?: string | null;
  death_date?: string | null;
}

export interface UserDetails {
  id: number;
  email: string;
  username: string;
  password: string;
  old_password : string;
  first_name: string;
  last_name: string;
  contact_number: string;
  address: string;
}

export interface Author extends AuthorDetails {
  id: number;
}

export type UserLoginData = {
  username: string;
  password: string;
};

export type Tokens = {
  access_token: string;
  refresh_token: string;
};

// The attributes of a book
export interface BookBase {
  title: string;
  description: string;
  isbn: string;
  dateOfPublication: string;
}

export interface BookOut extends BookBase {
  authorIds: number[];
  genreIds: number[];
  languageId: number;
  numberOfCopies: number;
}

export interface BookIn extends BookBase {
  id: number;
  authors: Author[];
  language: Language;
  genres: Genre[];
}

export interface Status {
  id: number;
  status: string;
}

export interface CopyOut {
  languageId: number;
  bookId: number;
  statusId: number;
}

export interface CopyIn {
  id: number;
  language: Language;
  book: BookIn;
  status: Status;
}

// The properties of Genre are stored in this type
export interface Genre {
  id: number;
  genre: string;
}

export interface GenreDetails {
  id: number;
  genre: string;
}

export interface ErrorObject {
  status: number;
  message: string;
}

export interface GenreMap {
  [id: number]: Genre;
}

export interface Language {
  id: number;
  language: string;
}
//Signup Attrubutes
export interface SignupData {
  email: string;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  contact_number: string;
  address: string;
}

//Language Attributes

export interface LanguageDetails {
  language: string | null;
  // Add other properties specific to the LanguageDetails type
}
export interface Language {
  id: number;
  language: string;
}

export interface BorrowedBase {
  issueDate: string;
  dueDate: string;
  returnDate: string | null;
}

export interface BorrowedIn extends BorrowedBase {
  id: number;
  copy: CopyIn;
  user: UserDetails;
}

export interface BorrowedOut extends BorrowedBase {
  copyId: number;
  userId: number | null;
}
