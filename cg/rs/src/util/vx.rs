#![allow(dead_code)]
use num::Float;
use std::iter::FromIterator;
use std::ops::*;

pub trait Vx<T>
where
    Self: Copy + Default,
    Self: FromIterator<T> + IntoIterator<Item = T>,
    Self: Index<usize, Output = T> + IndexMut<usize>,
    Self: Add<Output = Self>
        + Add<T, Output = Self>
        + Sub<Output = Self>
        + Sub<T, Output = Self>
        + Mul<Output = Self>
        + Mul<T, Output = Self>
        + Div<Output = Self>
        + Div<T, Output = Self>
        + Rem<Output = Self>
        + Rem<T, Output = Self>,
    T: Copy + Default + Float,
{
    fn dim() -> usize;

    fn of(value: T) -> Self;

    fn dot(&self, other: &Self) -> T {
        (*self * *other).into_iter().fold(T::zero(), |acc, v| acc + v)
    }

    fn mag(&self) -> T {
        self.dot(self).sqrt()
    }

    fn mag2(&self) -> T {
        self.dot(self)
    }

    fn dist(&self, other: &Self) -> T {
        (*self - *other).mag()
    }

    fn dist2(&self, other: &Self) -> T {
        (*self - *other).mag2()
    }

    fn cos(&self, other: &Self) -> T {
        self.dot(other) / (self.mag() * other.mag())
    }

    fn sin(&self, other: &Self) -> T {
        (T::one() - self.cos(other).powi(2)).sqrt()
    }

    fn rad(&self, other: &Self) -> T {
        self.cos(other).acos()
    }

    fn deg(&self, other: &Self) -> T {
        self.cos(other).acos().to_degrees()
    }

    fn norm(self) -> Self {
        self / self.mag()
    }
}

macro_rules! vector {
    ($v:ident $size:expr , { $($field:ident),+ }) => {
        #[repr(C)]
        #[derive(Copy, Clone, Debug)]
        pub struct $v<T> {
            $(pub $field: T),*
        }
        vector_default! { $v { $($field),+ } }
        vector_from_into! { $v $size , { $($field),+ } }
        vector_iterator! { from $v { $($field),+ } }
        vector_iterator! { into $v $size , { $($field),+ } }
        vector_index! { $v $size }
        vector_comparator! { $v { $($field),+ } }
        vector_operator! { unary $v { $($field),+ } Not::not }
        vector_operator! { unary $v { $($field),+ } Neg::neg }
        vector_operator! { binary $v { $($field),+ } Add::add }
        vector_operator! { binary $v { $($field),+ } Sub::sub }
        vector_operator! { binary $v { $($field),+ } Mul::mul }
        vector_operator! { binary $v { $($field),+ } Div::div }
        vector_operator! { binary $v { $($field),+ } Rem::rem }
        vector_operator! { assign $v { $($field),+ } AddAssign::add_assign }
        vector_operator! { assign $v { $($field),+ } SubAssign::sub_assign }
        vector_operator! { assign $v { $($field),+ } MulAssign::mul_assign }
        vector_operator! { assign $v { $($field),+ } DivAssign::div_assign }
        vector_operator! { assign $v { $($field),+ } RemAssign::rem_assign }

        impl<T: Default + Float> Vx<T> for $v<T> {
            fn dim() -> usize {
                $size
            }
            fn of(value: T) -> Self {
                Self { $($field: value),+ }
            }
        }
    };
}

macro_rules! vector_default {
    ($v:ident { $($field:ident),+ }) => {
        impl<T: Default> Default for $v<T> {
            fn default() -> Self { Self { $($field: T::default()),+ } }
        }
    };
}

macro_rules! vector_from_into {
    ($v:ident $size:expr , { $($field:ident),+ }) => {
        impl<'a, T: Copy> From<&'a [T; $size]> for $v<T> {
            fn from(slice: &'a [T; $size]) -> Self {
                let v: &$v<T> = From::from(slice);
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
                let s: &[T; $size] = From::from(vector);
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
    (into $v:ident $size:expr , { $($field:ident),+ }) => {
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

macro_rules! vector_index {
    ($v:ident $size:expr) => {
        vector_index! { base $v $size , usize => T }
        vector_index! { base $v $size , Range<usize> => [T] }
        vector_index! { base $v $size , RangeFrom<usize> => [T] }
        vector_index! { base $v $size , RangeInclusive<usize> => [T] }
        vector_index! { base $v $size , RangeTo<usize> => [T] }
        vector_index! { base $v $size , RangeToInclusive<usize> => [T] }
        vector_index! { base $v $size , RangeFull => [T] }
    };
    (base $v:ident $size:expr , $indexer:ty => $out:ty ) => {
        impl<T> Index<$indexer> for $v<T> {
            type Output = $out;
            fn index(&self, index: $indexer) -> &Self::Output {
                let ptr: &[T; $size] = From::from(self);
                &ptr[index]
            }
        }
        impl<T> IndexMut<$indexer> for $v<T> {
            fn index_mut(&mut self, index: $indexer) -> &mut Self::Output {
                let ptr: &mut [T; $size] = From::from(self);
                &mut ptr[index]
            }
        }
    };
}

macro_rules! vector_comparator {
    ($v:ident { $($field:ident),+ }) => {
        impl<T: Float> PartialOrd for $v<T> {
            fn partial_cmp(&self, rhs: &Self) -> Option<std::cmp::Ordering> {
                let self_mag_2 = $(self.$field * self.$field +)+ T::zero();
                let rhs_mag_2 = $(rhs.$field * rhs.$field +)+ T::zero();
                return match self_mag_2 - rhs_mag_2 {
                    x if x < T::zero() => Some(std::cmp::Ordering::Less),
                    x if x > T::zero() => Some(std::cmp::Ordering::Greater),
                    _ => Some(std::cmp::Ordering::Equal),
                };
            }
        }
        impl<T: PartialEq> PartialEq for $v<T> {
            fn eq(&self, rhs: &Self) -> bool {
                $(self.$field == rhs.$field)&&+
            }
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

vector! { V1 1 , { x }}
vector! { V2 2 , { x, y }}
vector! { V3 3 , { x, y, z }}
vector! { V4 4 , { x, y, z, w }}
