/**
 * This file contains custom data types and interfaces that are generic enough to be used multiple times throughout the project
 */

export interface AuthorDetails {
  first_name?: string | null;
  last_name?: string | null;
  birth_date?: string | null;
  death_date?: string | null;
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

export interface BookSaved extends BookBase {
  id: number;
  authors: Author[];
  language: Language;
  genres: Genre[];
}

// The properties of Genre are stored in this type
export interface Genre {
  id: number;
  genre: string;
}

export interface ErrorObject {
  status: number;
  message: string;
}

// GenreMap represents a map of Genre items. Id of genre is used as key
export interface GenreMap {
  [id: number]: Genre;
}

// The properties of a language are stored in this type
export interface Language {
  id: number;
  language: string;
}
