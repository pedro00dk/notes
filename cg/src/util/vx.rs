#![allow(dead_code)]
use num::Num;
use std::iter::FromIterator;
use std::ops::{Add, AddAssign, Neg, Not, Sub};

pub trait Vx<T>
where
    Self: Default,
    T: Copy + Default + Num,
{
    // fn dim() -> usize;
    // fn of(value: f32) -> Self;
}

#[repr(C)]
#[derive(Copy, Clone, Debug)]
pub struct V3<T> {
    pub x: T,
    pub y: T,
    pub z: T,
}

#[repr(C)]
#[derive(Copy, Clone, Debug)]
pub struct V4<T> {
    pub x: T,
    pub y: T,
    pub w: T,
}

macro_rules! vector_default {
    ($v:ident { $($field:ident),+ }) => {
        impl<T: Default> Default for $v<T> {
            fn default() -> Self { Self { $($field: T::default()),+ } }
        }
    };
}

macro_rules! vector_operator {
    (unary $v:ident { $($field:ident),+ } $trt:ident::$func:ident) => {
        impl<T: $trt<Output = T>> $trt for $v<T> {
            type Output = Self;
            fn $func(self) -> Self::Output {
                Self::Output { $($field: $trt::$func(self.$field)),+ }
            }
        }
    };
    (binary $v:ident { $($field:ident),+ } $trt:ident::$func:ident) => {
        impl<T: $trt<Output = T>> $trt for $v<T> {
            type Output = Self;
            fn $func(self, rhs: Self) -> Self::Output {
                Self::Output { $($field: $trt::$func(self.$field, rhs.$field)),+ }
            }
        }
        impl<T: $trt<Output = T> + Copy> $trt<T> for $v<T> {
            type Output = Self;
            fn $func(self, rhs: T) -> Self::Output {
                Self::Output { $($field: $trt::$func(self.$field, rhs)),+ }
            }
        }
    };
    (assign $v:ident { $($field:ident),+ } $trt:ident::$func:ident) => {
        impl<T: $trt> $trt for $v<T> {
            fn $func(&mut self, rhs: Self) {
                $($trt::$func(&mut self.$field, rhs.$field));*
            }
        }
        impl<T: $trt + Copy> $trt<T> for $v<T> {
            fn $func(&mut self, rhs: T) {
                $($trt::$func(&mut self.$field, rhs));*
            }
        }
    };
}

macro_rules! vector_from_into {
    ($v:ident { $($field:ident),+ } $size:expr) => {
        impl<'a, T: Copy> From<&'a [T; $size]> for $v<T> {
            fn from(slice: &'a [T; $size]) -> Self {
                let v: &V3<T> = From::from(slice);
                *v
            }
        }
        impl<'a, T> From<&'a [T; $size]> for &'a $v<T> {
            fn from(slice: &'a [T; $size]) -> Self {
                unsafe { std::mem::transmute(slice) }
            }
        }
        impl<'a, T> From<&'a mut [T; $size]> for &'a mut $v<T> {
            fn from(slice: &'a mut [T; $size]) -> Self {
                unsafe { std::mem::transmute(slice) }
            }
        }
        impl<'a, T: Copy> From<&'a $v<T>> for [T; $size] {
            fn from(vector: &'a $v<T>) -> Self {
                let s: &[T; 3] = From::from(vector);
                *s
            }
        }
        impl<'a, T> From<&'a $v<T>> for &'a [T; $size] {
            fn from(vector: &'a $v<T>) -> Self {
                unsafe { std::mem::transmute(vector) }
            }
        }
        impl<'a, T> From<&'a mut $v<T>> for &'a mut [T; $size] {
            fn from(vector: &'a mut $v<T>) -> Self {
                unsafe { std::mem::transmute(vector) }
            }
        }
    };
}

macro_rules! vector_iterator {
    (from $v:ident { $($field:ident),+ }) => {
        impl<T: Default> FromIterator<T> for $v<T> {
            fn from_iter<U: IntoIterator<Item = T>>(iter: U) -> Self {
                let mut iter = iter.into_iter();
                Self { $($field: iter.next().unwrap_or_default()),+ }
            }
        }
        impl<'a, T: 'a + Copy + Default> FromIterator<&'a T> for $v<T> {
            fn from_iter<U: IntoIterator<Item = &'a T>>(iter: U) -> Self {
                let mut iter = iter.into_iter();
                Self { $($field: *iter.next().unwrap_or(&T::default())),+ }
            }
        }
    };
    (into $v:ident { $($field:ident),+ } $size:expr) => {
        impl<T> IntoIterator for $v<T> {
            type Item = T;
            type IntoIter = std::array::IntoIter<T, $size>;
            fn into_iter(self) -> Self::IntoIter {
                std::array::IntoIter::new([ $(self.$field),* ])
            }
        }
        impl<T: Copy> IntoIterator for &$v<T> {
            type Item = T;
            type IntoIter = std::array::IntoIter<T, $size>;
            fn into_iter(self) -> Self::IntoIter {
                std::array::IntoIter::new([ $(self.$field),* ])
            }
        }

    };
}

vector_default! { V3 { x , y, z } }
vector_operator! { unary V3 { x , y, z } Not::not }
vector_operator! { unary V3 { x , y, z } Neg::neg }
vector_operator! { binary V3 { x , y, z } Add::add }
vector_operator! { binary V3 { x , y, z } Sub::sub }
vector_operator! { assign V3 { x , y, z } AddAssign::add_assign }
vector_from_into! { V3 { x , y, z } 3 }
vector_iterator! { from V3 { x , y, z } }
vector_iterator! { into V3 { x , y, z } 3 }
