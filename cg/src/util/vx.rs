#![allow(dead_code)]
use core::slice::SlicePattern;
use num::{Num, One, Zero};
// use std::fmt::Debug;
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
    (binary $v:ident { $($field:ident),+ } $trt:ident::$func:ident ) => {
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

vector_default! { V3 { x , y, z } }
vector_operator! { unary V3 { x , y, z } Not::not}
vector_operator! { unary V3 { x , y, z } Neg::neg}
vector_operator! { binary V3 { x , y, z } Add::add}
vector_operator! { binary V3 { x , y, z } Sub::sub}
vector_operator! { assign V3 { x , y, z } AddAssign::add_assign}

impl<T: Default> FromIterator<T> for V3<T> {
    fn from_iter<U: IntoIterator<Item = T>>(iter: U) -> Self {
        let mut iter = iter.into_iter();
        Self {
            x: iter.next().unwrap_or_default(),
            y: iter.next().unwrap_or_default(),
            z: iter.next().unwrap_or_default(),
        }
    }
}

impl<'a, T: Copy + Default> FromIterator<&'a T> for &'a V3<T> {
    fn from_iter<U: IntoIterator<Item = &'a T>>(iter: U) -> Self {
        let mut iter = iter.into_iter();
        Self {
            x: *iter.next().unwrap_or_else(|| &T::default()),
            y: *iter.next().unwrap_or_else(|| &T::default()),
            z: *iter.next().unwrap_or_else(|| &T::default()),
        }
    }
}

impl<T> IntoIterator for V3<T> {
    type Item = T;
    type IntoIter = std::array::IntoIter<T, 3>;

    fn into_iter(self) -> Self::IntoIter {
        std::array::IntoIter::new([self.x, self.y, self.z])
    }
}

impl<'a, T> IntoIterator for &'a V3<T> {
    type Item = &'a T;
    type IntoIter = std::slice::Iter<'a, T>;

    fn into_iter(self) -> Self::IntoIter {
        [self.x, self.y, self.z].into_iter()
    }
}
