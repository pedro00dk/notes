#![allow(dead_code)]
use num::{Num, One, Zero};
// use std::fmt::Debug;
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

macro_rules! vector_operation {
    (unary $v:ident { $($field:ident),+ } $trt:ident::$func:ident) => {
        impl<T: $trt<Output=T>> $trt for $v<T> {
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
                Self { $($field: $trt::$func(self.$field, rhs.$field)),+ }
            }
        }
        impl<T: $trt<Output = T> + Copy> $trt<T> for $v<T> {
            type Output = Self;
            fn $func(self, rhs: T) -> Self::Output {
                Self { $($field: $trt::$func(self.$field, rhs)),+ }
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
// vector_default! { V4 { x , y, z } }
vector_operation! { unary V3 { x , y, z } Not::not}
vector_operation! { unary V3 { x , y, z } Neg::neg}
vector_operation! { binary V3 { x , y, z } Add::add}
vector_operation! { binary V3 { x , y, z } Sub::sub}
vector_operation! { assign V3 { x , y, z } AddAssign::add_assign}

impl<T: Copy + Default + Num> Vx<T> for V3<T> {}

// impl<T: ops::Add<Output = T>> ops::Add for V3<T> {
//     type Output = Self;
//     fn add(self, rhs: Self) -> Self::Output {
//         Self { x: self.x + rhs.x, y: self.y + rhs.y, z: self.z + rhs.z }
//     }
// }
// impl<T: ops::Add<Output = T> + Copy> ops::Add<T> for V3<T> {
//     type Output = Self;
//     fn add(self, rhs: T) -> Self::Output {
//         Self { x: self.x + rhs, y: self.y + rhs, z: self.z + rhs }
//     }
// }
// impl<T: ops::AddAssign> ops::AddAssign for V3<T> {
//     fn add_assign(&mut self, rhs: Self) {
//         self.x += rhs.x;
//         self.y += rhs.y;
//         self.z += rhs.z;
//     }
// }
// impl<T: ops::AddAssign + Copy> ops::AddAssign<T> for V3<T> {
//     fn add_assign(&mut self, rhs: T) {
//         self.x += rhs;
//         self.y += rhs;
//         self.z += rhs;
//     }
// }
