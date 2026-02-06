// book.model.ts

import { Category } from "./category";
import { Tag } from "./tag";

export interface BookCategoryLink {
  category_id: number;
}

export interface Book {
  id: number;
  title: string;
  author?: string;
  description?: string;
  isbn?: string;
  published_year?: string;
  quantity: number;
  cover_url?: string;

  category_id?: number;
  tag?: Tag[];
}

export interface BookFilter {
  title?: string;
  author?: string;
  published_after?: number;
  published_before?: number;
  category_ids?: number[];
  tag_ids?: number[];
}

export interface BorrowedBook {
  loan_id: number;
  book_id: number;
  title: string;
  author: string;
  description: string;
  isbn: string;
  published_year: number;
  category_id: number;
  cover_url: string;
  loan_date: string;
  due_date: string;
  return_date?: string;
  status: string;
  book_quantity?: number;
}
