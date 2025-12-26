// book.model.ts

import { Category } from "./category";

export interface Book {
  id: number;
  title: string;
  author?: string;
  description?: string;
  isbn?: string;
  published_year?: number;
  quantity: number;
  cover_url?: string;

  category?: Category;
}

export interface BookFilter {
  title?: string;
  author?: string;
  published_after?: number;
  published_before?: number;
  category_ids?: number[];
  tag_ids?: number[];
}
