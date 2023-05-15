/**
 * This file contains custom data types and interfaces that are generic enough to be used multiple times throughout the project
 */

 export interface AuthorDetails {
    first_name?: string|null,
    last_name?: string|null,
    date_of_birth?: string|null,
    date_of_death?:string|null
}

export interface Author extends AuthorDetails {
    id: number;
}

export type UserLoginData = {
    username:string,
    password:string
}

export type Tokens = {
    access_token:string
    refresh_token:string
}

// The attributes of a book
export interface Book {
    title: string;
    authorId: number;
    summary: string;
    isbn: string;
    languageId: number;
    genreIds: number[];
}

// An object of book that is saved in backend server will have an id attribute
export interface BookSaved extends Book{
    id: number;
}

// The properties of Genre are stored in this type
export interface Genre {
    id: number;
    name: string;
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
    name: string;
}
